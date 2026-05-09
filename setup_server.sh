#!/bin/bash
# =============================================================================
# ROSClaw Wiki — Production Server Setup Script
# =============================================================================
# 用途：在 Ubuntu 服务器上一键部署 ROSClaw Wiki 生产环境
# 前提：项目代码已放在 ~/rosclaw/rosclaw-wiki 目录下
# 运行：bash setup_server.sh
# =============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_DIR="${HOME}/rosclaw/rosclaw-wiki"
APP_DIR="/opt/rosclaw-wiki"
DOMAIN="api.rosclaw.io"
EMAIL="admin@rosclaw.io"

# =============================================================================
# 1. 项目简介（给部署工程师看的）
# =============================================================================
cat <<'INTRO'

================================================================================
                    ROSClaw Wiki — 部署说明
================================================================================

【项目定位】
ROSClaw Wiki 是具身智能（Embodied AI）领域的物理常识防火墙与知识中枢。
它将论文、代码仓库、机器人 URDF 规范转化为结构化知识图谱，为 LLM Agent
提供物理世界约束（扭矩、电流、温度、摩擦等）的实时查询服务。

【核心架构】
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Nginx     │────▶│  FastAPI    │────▶│   SeekDB    │
  │  (443/80)   │     │  (8000)     │     │  (2881)     │
  └─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  R2 (S3)    │  ← 预签名 URL 上传
                     └─────────────┘

【服务组件】
  1. nginx      — 反向代理 + SSL 终止
  2. rosclaw-api — FastAPI 应用服务（Gunicorn + Uvicorn）
  3. seekdb     — 向量/混合搜索引擎
  4. certbot    — Let's Encrypt 自动续期

【关键文件】
  • docker-compose.prod.yml  — 生产编排
  • Dockerfile.prod          — 生产镜像
  • nginx/rosclaw.conf       — Nginx 配置
  • commercial_api.py        — API 入口
  • wiki/                    — 800+ Wiki 页面
  • wiki/judgments/index.json — 1026 条物理判据

【部署要求】
  • Ubuntu 22.04+ / Debian 12+
  • 至少 2 CPU / 4GB RAM / 20GB 磁盘
  • 域名 api.rosclaw.io 已解析到本机 IP
  • 开放端口：22(SSH), 80(HTTP), 443(HTTPS)

================================================================================
INTRO

log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}   $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# 2. 前置检查
# =============================================================================
log_info "Step 1/10: 环境检查"

# 检查是否在正确的目录
if [ ! -f "${PROJECT_DIR}/docker-compose.prod.yml" ]; then
    log_error "项目目录 ${PROJECT_DIR} 不存在或缺少 docker-compose.prod.yml"
    log_info "请确认项目已拷贝到 ~/rosclaw/rosclaw-wiki 后再运行此脚本"
    exit 1
fi
log_ok "项目目录检查通过"

# 检查 root/sudo
if [ "$EUID" -ne 0 ]; then
    log_warn "当前非 root 用户，部分操作需要 sudo 权限"
    if ! sudo -n true 2>/dev/null; then
        log_error "sudo 需要密码，请先配置免密 sudo 或切换到 root 运行"
        exit 1
    fi
fi

# 检查域名解析
SERVER_IP=$(curl -s -4 ifconfig.me 2>/dev/null || echo "unknown")
log_info "本机公网 IP: ${SERVER_IP}"
log_info "请确认域名 ${DOMAIN} 已解析到此 IP"

# =============================================================================
# 3. 系统依赖安装
# =============================================================================
log_info "Step 2/10: 安装系统依赖 (Docker, Nginx, Certbot)"

# 更新包索引
sudo apt-get update -y

# 安装基础工具
sudo apt-get install -y --no-install-recommends \
    git curl wget ca-certificates gnupg lsb-release \
    nginx certbot python3-certbot-nginx

log_ok "基础工具安装完成"

# 安装 Docker（如果未安装）
if ! command -v docker &>/dev/null; then
    log_info "安装 Docker..."
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker "${USER}" || true
    log_ok "Docker 安装完成"
else
    log_ok "Docker 已存在: $(docker --version)"
fi

# 安装 Docker Compose（如果未安装）
if ! command -v docker-compose &>/dev/null; then
    log_info "安装 Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    log_ok "Docker Compose 安装完成"
else
    log_ok "Docker Compose 已存在: $(docker-compose --version)"
fi

# =============================================================================
# 4. 项目部署到 /opt
# =============================================================================
log_info "Step 3/10: 部署项目到 ${APP_DIR}"

sudo mkdir -p "${APP_DIR}"
sudo cp -r "${PROJECT_DIR}"/* "${APP_DIR}/"
sudo chown -R "${USER}:${USER}" "${APP_DIR}"
cd "${APP_DIR}"

log_ok "项目已部署到 ${APP_DIR}"

# =============================================================================
# 5. 环境变量配置
# =============================================================================
log_info "Step 4/10: 配置环境变量"

if [ ! -f ".env" ]; then
    cp .env.example .env
    log_warn ".env 文件已从模板创建，请务必编辑填入实际值！"
fi

# 显示当前 .env 内容（脱敏）
log_info "当前 .env 配置（请检查是否已填入实际值）："
grep -E "^[A-Z]" .env | sed 's/=.*/=***/' || true

cat <<'ENV_HELP'

┌─────────────────────────────────────────────────────────────────────────────┐
│                        .env 配置说明                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 必填项（至少配置一个 LLM API）：                                              │
│   ANTHROPIC_API_KEY=sk-ant-xxx          # Claude API                        │
│   DEEPSEEK_API_KEY=sk-xxx               # DeepSeek API                      │
│   OPENAI_API_KEY=sk-xxx                 # OpenAI API                        │
│                                                                             │
│ 服务器端必填项：                                                             │
│   ROSCLAW_API_KEY=rw_sk_xxx             # API Key 用于鉴权                  │
│   R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com  # Cloudflare R2         │
│   R2_ACCESS_KEY_ID=xxx                  # R2 Access Key                     │
│   R2_SECRET_ACCESS_KEY=xxx              # R2 Secret Key                     │
│   R2_BUCKET=rosclaw-wiki                # R2 存储桶名称                      │
│                                                                             │
│ 可选项：                                                                     │
│   PADDLEOCR_API_URL=xxx                 # PaddleOCR 端点（PDF OCR）          │
│   PADDLEOCR_API_TOKEN=xxx               # PaddleOCR Token                   │
└─────────────────────────────────────────────────────────────────────────────┘

ENV_HELP

log_warn "如果 .env 中的值还是 *** 占位符，请先编辑 ${APP_DIR}/.env"
read -r -p "按 Enter 继续（或 Ctrl+C 编辑 .env 后再运行）..."

# =============================================================================
# 6. Docker 构建与启动
# =============================================================================
log_info "Step 5/10: 构建并启动 Docker 服务"

sudo docker-compose -f docker-compose.prod.yml build --no-cache
sudo docker-compose -f docker-compose.prod.yml up -d

log_info "等待服务启动（15 秒）..."
sleep 15

# 检查容器状态
log_info "容器状态："
sudo docker-compose -f docker-compose.prod.yml ps

# 健康检查
log_info "Step 6/10: 健康检查"
if curl -s http://localhost:8000/wiki/v1/health | grep -q "ok"; then
    log_ok "API 服务健康检查通过"
else
    log_warn "API 服务暂未响应，可能还在启动中"
    log_info "查看日志: sudo docker logs rosclaw-api"
fi

# =============================================================================
# 7. Nginx 配置
# =============================================================================
log_info "Step 7/10: 配置 Nginx 反向代理"

sudo cp "${APP_DIR}/nginx/rosclaw.conf" /etc/nginx/sites-available/rosclaw

# 确保 sites-enabled 存在
sudo mkdir -p /etc/nginx/sites-enabled

# 移除默认配置（可选）
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
fi

# 启用 rosclaw 配置
if [ ! -f /etc/nginx/sites-enabled/rosclaw ]; then
    sudo ln -s /etc/nginx/sites-available/rosclaw /etc/nginx/sites-enabled/rosclaw
fi

# 测试配置
if sudo nginx -t; then
    log_ok "Nginx 配置测试通过"
    sudo systemctl reload nginx || sudo service nginx reload
    log_ok "Nginx 已重新加载"
else
    log_error "Nginx 配置测试失败"
    exit 1
fi

# =============================================================================
# 8. SSL 证书申请
# =============================================================================
log_info "Step 8/10: 申请 SSL 证书 (Let's Encrypt)"

if sudo certbot --nginx -d "${DOMAIN}" --non-interactive --agree-tos --email "${EMAIL}"; then
    log_ok "SSL 证书申请成功"
else
    log_warn "SSL 证书申请失败（可能域名解析未生效）"
    log_info "域名解析生效后，手动运行: sudo certbot --nginx -d ${DOMAIN}"
fi

# =============================================================================
# 9. 数据导入（可选）
# =============================================================================
log_info "Step 9/10: 数据导入（如果存在 seekdb_import.jsonl）"

if [ -f "${APP_DIR}/data/seekdb_import.jsonl" ]; then
    log_info "发现 seekdb_import.jsonl，准备导入..."
    sudo docker exec rosclaw-api python import_to_seekdb.py \
        --input data/seekdb_import.jsonl --backend seekdb || true
    log_ok "数据导入完成"
else
    log_warn "未找到 data/seekdb_import.jsonl，跳过数据导入"
    log_info "后续可手动导入: docker exec rosclaw-api python import_to_seekdb.py ..."
fi

# =============================================================================
# 10. 最终验证
# =============================================================================
log_info "Step 10/10: 最终验证"

cat <<'VERIFY'

================================================================================
                          部署验证清单
================================================================================
VERIFY

# 检查各组件
CHECKS=0
PASSED=0

check() {
    CHECKS=$((CHECKS + 1))
    if eval "$2" >/dev/null 2>&1; then
        log_ok "$1"
        PASSED=$((PASSED + 1))
    else
        log_error "$1"
    fi
}

check "Docker 运行中"       "sudo docker info"
check "Nginx 运行中"        "sudo systemctl is-active nginx || sudo service nginx status"
check "SeekDB 容器运行中"   "sudo docker ps | grep rosclaw-seekdb"
check "API 容器运行中"      "sudo docker ps | grep rosclaw-api"
check "API 本地健康检查"    "curl -s http://localhost:8000/wiki/v1/health | grep -q ok"

# 如果域名解析已生效，测试公网访问
if curl -s "https://${DOMAIN}/wiki/v1/health" | grep -q "ok" 2>/dev/null; then
    log_ok "公网 HTTPS 访问正常: https://${DOMAIN}"
    PASSED=$((PASSED + 1))
else
    log_warn "公网 HTTPS 暂未可用（域名解析可能未生效）"
fi
CHECKS=$((CHECKS + 1))

echo ""
echo "================================================================================"
log_info "验证结果: ${PASSED}/${CHECKS} 项通过"
echo "================================================================================"

# =============================================================================
# 常用命令速查
# =============================================================================
cat <<'COMMANDS'

┌─────────────────────────────────────────────────────────────────────────────┐
│                        常用运维命令                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 查看日志                                                                    │
│   sudo docker logs -f rosclaw-api          # API 服务日志                   │
│   sudo docker logs -f rosclaw-seekdb       # SeekDB 日志                    │
│   sudo tail -f /var/log/nginx/access.log   # Nginx 访问日志                 │
│                                                                             │
│ 服务管理                                                                    │
│   sudo docker-compose -f /opt/rosclaw-wiki/docker-compose.prod.yml ps       │
│   sudo docker-compose -f /opt/rosclaw-wiki/docker-compose.prod.yml restart  │
│   sudo docker-compose -f /opt/rosclaw-wiki/docker-compose.prod.yml down     │
│   sudo docker-compose -f /opt/rosclaw-wiki/docker-compose.prod.yml up -d    │
│                                                                             │
│ 健康检查                                                                    │
│   curl https://api.rosclaw.io/wiki/v1/health                                │
│   curl -H "X-API-Key: YOUR_KEY" https://api.rosclaw.io/wiki/v1/search \     │
│        -H "Content-Type: application/json" -d '{"query":"test"}'            │
│                                                                             │
│ SSL 证书                                                                    │
│   sudo certbot renew --dry-run             # 测试续期                       │
│   sudo certbot certificates                # 查看证书状态                   │
│                                                                             │
│ 数据备份                                                                    │
│   sudo docker exec rosclaw-seekdb seekdb-backup > backup.sql                │
│   sudo tar czf wiki-backup-$(date +%Y%m%d).tar.gz /opt/rosclaw-wiki/wiki    │
│                                                                             │
│ 压力测试                                                                    │
│   sudo apt-get install wrk                                                  │
│   wrk -t4 -c50 -d30s --latency https://api.rosclaw.io/wiki/v1/health        │
└─────────────────────────────────────────────────────────────────────────────┘

COMMANDS

echo ""
log_ok "ROSClaw Wiki 部署脚本执行完毕！"
log_info "项目地址: ${APP_DIR}"
log_info "API 地址: https://${DOMAIN}"
log_info "GitHub:   https://github.com/ros-claw/rosclaw-wiki"
echo ""
