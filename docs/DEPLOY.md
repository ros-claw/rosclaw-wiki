# ROSClaw Wiki 生产部署指南

> 覆盖 Cloudflare Tunnel、R2 存储、Gunicorn/Flask 服务管理的完整部署文档。

---

## 架构概览

```
用户 → wiki.rosclaw.io ──Cloudflare Tunnel──→ cloudflared ──→ localhost:5000 (Flask wiki UI)
     → api.rosclaw.io  ──Nginx/Gunicorn────→ localhost:8000 (FastAPI commercial_api)
     → www.rosclaw.io  ──Vercel CDN────────→ Next.js 前端
```

| 组件 | 域名 | 端口 | 技术 |
|------|------|------|------|
| Wiki 可视化界面 | `wiki.rosclaw.io` | 5000 | Flask + SocketIO |
| API 服务 | `api.rosclaw.io` | 8000 | FastAPI + Gunicorn |
| 前端网站 | `www.rosclaw.io` | 443 | Vercel (Next.js) |
| R2 存储 | — | — | Cloudflare R2 (S3-compatible) |

---

## 1. Cloudflare Tunnel 部署

### 1.1 Dashboard 创建 Tunnel

1. 登录 [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com)
2. Networks → Tunnels → **Create a tunnel**
3. Tunnel name: `rosclaw-wiki`
4. 选择 Connector: **Debian**（Ubuntu 兼容）
5. 复制 token（形如 `eyJhIjoi...`）

### 1.2 配置 Public Hostname

在 Tunnel 详情页 → **Public Hostname** → Add a public hostname：

| 字段 | 值 |
|------|-----|
| Subdomain | `wiki` |
| Domain | `rosclaw.io` |
| Path | 留空 |
| Type | `HTTP` |
| URL | `localhost:5000` |

保存后 Dashboard 显示：
```
wiki.rosclaw.io → http://localhost:5000
```

### 1.3 服务器安装与启动

```bash
# 安装 cloudflared
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | \
  sudo tee /usr/share/keyrings/cloudflare-main.gpg > /dev/null

echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] \
  https://pkg.cloudflare.com/cloudflared any main' | \
  sudo tee /etc/apt/sources.list.d/cloudflared.list

sudo apt-get update && sudo apt-get install cloudflared

# 安装为系统服务（用 Dashboard 给的 token）
sudo cloudflared service install <YOUR_TOKEN_HERE>

# 启动并设置开机自启
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# 验证状态
sudo systemctl status cloudflared
# 期望输出: Active: active (running)
```

### 1.4 SSL/TLS 设置

Cloudflare Dashboard → `rosclaw.io` → **SSL/TLS → Overview**：

- **Encryption mode**: 选择 `Full` 或 `Full (strict)`
- 不要选 `Flexible`（会导致无限重定向）
- 不要选 `Off`（无加密）

### 1.5 DNS 检查

Tunnel 会自动管理 DNS，不需要手动添加记录。但需确保：

- 删除旧的 A 记录 `wiki`（如果有）
- DNS 中的 `wiki` 记录由 Tunnel 自动创建为 CNAME

验证：
```bash
dig wiki.rosclaw.io +short
# 期望输出: <tunnel-id>.cfargotunnel.com（不是服务器 IP）
```

---

## 2. Flask Wiki UI 服务

### 2.1 启动 Flask

```bash
cd ~/rosclaw/rosclaw-wiki

# 安装依赖
pip install flask flask-socketio pyyaml

# 后台启动
nohup python3 -m web_ui.app > web_ui.log 2>&1 &

# 验证端口
ss -tlnp | grep 5000
# 期望: LISTEN 0.0.0.0:5000
```

### 2.2 设为 systemd 服务（推荐）

创建 `/etc/systemd/system/rosclaw-wiki-ui.service`：

```ini
[Unit]
Description=ROSClaw Wiki UI (Flask)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/rosclaw/rosclaw-wiki
ExecStart=/home/ubuntu/rosclaw/rosclaw-wiki/.venv/bin/python -m web_ui.app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable rosclaw-wiki-ui
sudo systemctl start rosclaw-wiki-ui
```

---

## 3. FastAPI / Gunicorn 服务

### 3.1 Gunicorn 启动配置

```bash
cd ~/rosclaw/rosclaw-wiki

# 启动（已配置 preload_app 缓存 code_graph.json）
gunicorn commercial_api:app \
  --bind 127.0.0.1:8000 \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --preload \
  --access-logfile - \
  --error-logfile -
```

### 3.2 重载（代码更新后）

```bash
# 修改代码后，graceful reload 使缓存刷新
sudo kill -HUP $(pgrep -f 'gunicorn.*commercial_api')
```

---

## 4. R2 存储配置

### 4.1 环境变量

**方式一：直接导出（临时）**

```bash
export R2_ENDPOINT="https://<account-id>.r2.cloudflarestorage.com"
export R2_ACCESS_KEY_ID="<your-access-key-id>"
export R2_SECRET_ACCESS_KEY="<your-secret-access-key>"
export R2_BUCKET="rosclaw-wiki"
```

**方式二：`.env` 文件（推荐，本地开发）**

```bash
cd ~/rosclaw/rosclaw-wiki
cat > .env << 'EOF'
R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=<your-access-key-id>
R2_SECRET_ACCESS_KEY=<your-secret-access-key>
R2_BUCKET=rosclaw-wiki
EOF
```

**方式三：systemd 环境变量（生产环境）**

在 `/etc/systemd/system/rosclaw-wiki-ui.service` 的 `[Service]` 段添加：

```ini
Environment="R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com"
Environment="R2_ACCESS_KEY_ID=<your-access-key-id>"
Environment="R2_SECRET_ACCESS_KEY=<your-secret-access-key>"
Environment="R2_BUCKET=rosclaw-wiki"
```

然后 `sudo systemctl daemon-reload && sudo systemctl restart rosclaw-wiki-ui`。

> **安全提示**：`.env` 文件已加入 `.gitignore`，不会被提交到 git。切勿将密钥写入代码文件。

### 4.2 设备端：打包 + 上传

```bash
# 1. 打包本地 wiki 变更
python3 batch_sync.py device-package --name batch_name

# 2. 上传到 R2
python3 batch_sync.py device-upload \
  --tar submissions/batch_name_YYYYMMDD_HHMMSS.tar.gz \
  --r2-prefix submissions
```

### 4.3 生产端：从 R2 合并

```bash
# 下载并合并 submission
python3 batch_sync.py production-merge \
  --r2-key submissions/batch_name_YYYYMMDD_HHMMSS.tar.gz
```

---

## 5. Docker Compose 部署（推荐 / 当前生产方案）

`api.rosclaw.io` 目前就是用 `docker-compose.prod.yml` 跑的。三个服务：

| 服务 | 镜像 / 来源 | 端口 | 角色 |
|------|-------------|------|------|
| `rosclaw-api` | `Dockerfile.prod` 本地构建（python:3.11-slim） | 8000 | FastAPI + Gunicorn (`commercial_api:app`) |
| `rosclaw-seekdb` | `oceanbase/seekdb:latest` | 2881 | 向量库 |
| `rosclaw-redis` | `redis:7-alpine` | 6379 | Job/缓存 |

### 5.1 准备 `.env`

把仓库根目录的 `.env.example` 复制为 `.env`，填上：

```bash
# R2（device → admin merge 必需，详见 docs/ADMIN_BATCH_SYNC.md）
R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=<key>
R2_SECRET_ACCESS_KEY=<secret>
R2_BUCKET=rosclaw-wiki

# 一般不用改
WIKI_ROOT=/app/wiki
WIKI_BACKEND=seekdb
SEEKDB_MODE=server
```

> `docker compose` 启动时会自动读这个 `.env` 完成变量替换。**不要把 `.env` 提交到 git**（仓库 `.gitignore` 已经覆盖）。

### 5.2 构建 + 启动

```bash
cd ~/rosclaw/rosclaw-wiki
sudo docker compose -f docker-compose.prod.yml build rosclaw-api
sudo docker compose -f docker-compose.prod.yml up -d
sudo docker compose -f docker-compose.prod.yml ps
```

健康检查：

```bash
curl -s http://localhost:8000/v1/health | jq
curl -s https://api.rosclaw.io/v1/health | jq      # 经过 host nginx + Cloudflare
curl -s https://api.rosclaw.io/wiki/v1/batch/list  # 应返回 {"status":"ok","batches":[]}
```

### 5.3 升级流程（修改后端代码后）

```bash
cd ~/rosclaw/rosclaw-wiki
git pull origin main
sudo docker compose -f docker-compose.prod.yml build rosclaw-api
sudo docker compose -f docker-compose.prod.yml up -d rosclaw-api
```

容器 healthcheck 通过后请求会自动恢复。若只改 `wiki/` 或 `data/`（绑定挂载），无需重建镜像，但 `gunicorn` 仍需 `kill -HUP` 才会清空 `code_graph.json` 的 preload 缓存：

```bash
sudo docker exec rosclaw-api kill -HUP 1
```

### 5.4 关键挂载与权限

```yaml
volumes:
  - ./wiki:/app/wiki      # RW —— admin batch merge 会写新页面进来
  - ./data:/app/data      # RW —— SQLite / code_graph.json / submissions 缓存
```

> 历史教训：早期 `/app/wiki` 挂的是 `:ro`，admin UI 一点 merge 就 `[Errno 30] Read-only file system`。改成 RW 后批量合并才能落盘。

### 5.5 nginx 上游超时

`commercial_api.batch_merge` 已经把慢的 seekdb embedding 放到 BackgroundTasks，但 nginx 默认 `proxy_read_timeout 60s` 仍然偏紧。生产 `/etc/nginx/sites-enabled/rosclaw` 给 `/wiki/v1/batch/` 单独抬到 600s：

```nginx
location /wiki/v1/batch/ {
  proxy_pass http://rosclaw_api;
  proxy_read_timeout 600s;
  proxy_send_timeout 600s;
  ...
}
```

### 5.6 老方案（裸跑 gunicorn）

第 3 节描述的 systemd 直接跑 `gunicorn` 仍然能用，但**当前生产没在用**——保留是为了灾备 / 单机本地开发。两个方案不要同时启动 `:8000`，否则会端口冲突。

---

## 6. 故障排查

| 现象 | 原因 | 修复 |
|------|------|------|
| `ERR_TUNNEL_CONNECTION_FAILED` | Tunnel 未运行或 token 错误 | `sudo systemctl status cloudflared` |
| `{"detail":"Not Found"}` | 请求到了 FastAPI (8000) 而非 Flask (5000) | 检查 Tunnel Public Hostname URL 是否为 `localhost:5000` |
| `502 Bad Gateway` | Flask 未在 5000 端口运行 | `ss -tlnp | grep 5000` |
| 浏览器显示"不安全" | SSL/TLS 模式为 Off/Flexible | Dashboard → SSL/TLS → 改为 Full |
| `dig` 返回服务器 IP | 旧 A 记录未删除 | DNS 中删除 `wiki` A 记录，让 Tunnel 自动管理 |
| CORS 报错 | wiki.rosclaw.io 不在 allow_origins | 检查 `commercial_api.py` 的 `CORS_ORIGINS` 环境变量 |
| wiki 页面点击 404 | 孤儿链接（orphaned wikilink）| 运行 `python3 -c "import wiki_engine; wiki_engine.list_pages('wiki')"` 检查 |
| R2 上传报错 `KeyError: R2_ENDPOINT` | 环境变量未设置 | 确认 `.env` 文件存在且已 source |
| wiki.rosclaw.io 返回 `{"detail":"Not Found"}` | Tunnel 指向了 8000 而非 5000 | Dashboard 检查 Public Hostname URL 为 `http://localhost:5000` |

---

## 7. Wiki 维护命令

### 7.1 检查知识健康

```bash
# 统计页面数和孤儿链接
python3 -c "
import re
from pathlib import Path
from collections import Counter

wiki = Path('wiki')
pages = list(wiki.rglob('*.md'))
print(f'总页面: {len(pages)}')

existing = {}
for f in pages:
    existing[f.stem.lower()] = f.stem
    m = re.search(r'^title: (.+)$', f.read_text(), re.M)
    if m: existing[m.group(1).strip().lower()] = m.group(1).strip()

orphans = Counter()
for f in pages:
    for m in re.finditer(r'\[\[([^\]|]+)\]\]', f.read_text()):
        link = m.group(1).strip()
        if link.lower() not in existing:
            orphans[link] += 1

print(f'孤儿链接: {sum(orphans.values())} (种类: {len(orphans)})')
for l, c in orphans.most_common(10):
    print(f'  {c:4d} {l}')
"
```

### 7.2 更新 wiki 索引

```bash
python3 -c "
import wiki_engine
wiki_engine.update_index('wiki')
"
```

### 7.3 重新导出知识图谱

```bash
python3 -c "
from graph_exporter import export_graph
export_graph('wiki', output_dir='data/graph_export', fmt='json')
"
```
