# Admin Batch Sync Workflow

> 端到端讲清楚：开发设备产出 → R2 中转 → 生产 admin UI 合并 → 自动归档。

---

## 概览

```
┌──────────────────┐   tarball + manifest    ┌──────────────────┐
│ 开发设备         │ ─────────────────────►  │ Cloudflare R2    │
│ batch_sync.py    │      device-upload      │ rosclaw-wiki     │
│ device-package   │                         │ submissions/     │
└──────────────────┘                         └────────┬─────────┘
                                                       │ presigned GET
                                          ┌────────────▼─────────┐
                                          │ www.rosclaw.io/admin │
                                          │ Batch Sync tab       │
                                          │  list / preview /    │
                                          │  merge / reject      │
                                          └────────┬─────────────┘
                                                   │ FastAPI
                                          ┌────────▼─────────────┐
                                          │ api.rosclaw.io       │
                                          │ /wiki/v1/batch/*     │
                                          │ (Docker Compose)     │
                                          └────────┬─────────────┘
                                                   │ merge writes
                                ┌──────────────────┼──────────────┐
                                ▼                  ▼              ▼
                       wiki/ (md files)     data/code_graph    SQLite +
                       (host bind mount)    .json (canonical)  seekdb (bg)

                                                   │ archive
                                          ┌────────▼─────────────┐
                                          │ R2 submissions/      │
                                          │ processed/           │
                                          └──────────────────────┘
```

R2 bucket：`rosclaw-wiki`，前缀：`submissions/`（待处理）+ `submissions/processed/`（已合并）。

---

## 设备端：打包 + 上传

```bash
# 把本地 wiki/ + data/code_graph_batch_*.json + data/judgments.jsonl + data/wiki_pages.jsonl 打成一个 tarball
.venv/bin/python batch_sync.py device-package --name vln_expansion

# 输出: submissions/vln_expansion_YYYYMMDD_HHMMSS.tar.gz

# 上传到 R2（默认前缀 submissions/）
.venv/bin/python batch_sync.py device-upload \
  --tar submissions/vln_expansion_YYYYMMDD_HHMMSS.tar.gz
```

需要在设备 `.env`（或 shell environment）里有：

```bash
R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=<key>
R2_SECRET_ACCESS_KEY=<secret>
R2_BUCKET=rosclaw-wiki
```

**Tip — code-graph 维度**：`production_merge` 把 `cg_files = manifest.get("code_graphs", [])` 当成空时会显示 `code_graph_merged: false / skipped`。这是按 manifest 走的——device 端要确保 `data/code_graph_batch_<name>.json` 存在，`device-package` 才会把它放进 tarball 的 `code_graphs` 列表。**纯 wiki/judgments 的 batch 报告 skipped 是正常现象。**

---

## 管理员端：在 admin UI 操作

URL：[https://www.rosclaw.io/admin](https://www.rosclaw.io/admin) → 顶部 tab 切到 **Batch Sync**。

### 列表（List）

- 调用 `GET /wiki/v1/batch/list`
- 服务端：`r2_sync.list_submissions_detailed("submissions")`，过滤掉 `/processed/` 前缀的对象
- 每行显示：`batch_name`、R2 LastModified（作为 created_at）、size
- 已合并的 batch 不再显示——见下面的归档逻辑

### 预览（Preview）

- 调用 `POST /wiki/v1/batch/preview {"batch_id": "submissions/foo.tar.gz"}`
- 服务端：生成 R2 presigned GET URL → 下载 tarball → 用 tarfile 抽取 `manifest.json` → 返回 manifest 内容
- 不写任何文件、不修改数据库——只是预览
- 失败时返回 `{"status":"error","message":"..."}`

### 合并（Merge）

- 调用 `POST /wiki/v1/batch/merge {"batch_id": "submissions/foo.tar.gz"}`
- 同步路径（~10 秒就返回）：
  1. `production_merge(skip_seekdb=True)`：复制 `wiki/*.md`、合并 `data/code_graph.json`、INSERT OR REPLACE 进 SQLite `wiki_pages` + `judgments` 表、`engine.update_index()` 重建 `wiki/index.md`
  2. 把 tarball 落到 `data/submissions/<key>.tar.gz` 留个本地缓存
- 异步路径（BackgroundTasks）：
  3. `reindex_seekdb_from_tarball(tar_path)`：用同一份 tarball、调 `pyseekdb` `Collection.upsert(ids=[...], documents=[...], metadatas=[...], embeddings=...)` 把向量灌进 `seekdb` 容器
  4. `move_object("submissions/foo.tar.gz", "submissions/processed/foo.tar.gz")` —— 把 R2 上的源文件搬到 processed/，下次列表就不会再出现
- 响应体：

```json
{
  "status": "ok",
  "result": {
    "batch_name": "vln_expansion",
    "wiki_merged": 1032,
    "wiki_conflicts": 1032,
    "code_graph_merged": false,
    "judgments_imported": 14,
    "wiki_pages_imported": 1032,
    "errors": [],
    "seekdb_reindex": "scheduled",
    "archived_to": "submissions/processed/vln_expansion_20260511_141711.tar.gz"
  }
}
```

`wiki_conflicts` 跟 `wiki_merged` 一样多表示"全是覆盖"——上一次已经合过、本次再合不会丢数据。**多次 merge 同一个 batch 是幂等的**：文件 `shutil.copy2` 重写、code_graph 按 (id, source, target) 去重、SQLite `INSERT OR REPLACE`。

### 拒绝（Reject）

- 调用 `POST /wiki/v1/batch/reject {"batch_id": "submissions/foo.tar.gz"}`
- 服务端：`r2_sync.delete_object(key)` 直接把 R2 对象删掉（无归档、不可恢复）
- 用于丢弃损坏或不想要的 submission

---

## 重试 & 恢复

### 我想重跑一个已经归档的 batch

```bash
# 在生产服务器
ssh ubuntu@<prod-ip>
sudo docker exec rosclaw-api python3 -c '
from r2_sync import move_object
move_object("submissions/processed/foo.tar.gz", "submissions/foo.tar.gz")'
```

把它移回 `submissions/`，admin UI 会重新看到、可以再 merge。

### 我点了 reject 但反悔

R2 free tier 没有 versioning；删了就是删了。请先 preview 确认 manifest 再 reject。

### 后台 seekdb reindex 跑挂了怎么办

- 检查 `sudo docker logs rosclaw-api | grep -i seekdb`
- 重跑：

```bash
sudo docker exec rosclaw-api python3 -c '
from batch_sync import reindex_seekdb_from_tarball
reindex_seekdb_from_tarball("/app/data/submissions/foo.tar.gz")'
```

`data/submissions/` 是容器内的本地缓存（host `./data/submissions/` 挂进来的），merge 阶段下载下来的 tarball 都在这里。

---

## 端点对照表

| 方法 | 路径 | 用途 |
|------|------|------|
| GET  | `/wiki/v1/batch/list` | 列出待合并 batch（不含 `processed/`） |
| POST | `/wiki/v1/batch/preview` | 只读：拉 manifest 看 |
| POST | `/wiki/v1/batch/merge` | 写：合并到生产 + 归档 + 后台 seekdb 同步 |
| POST | `/wiki/v1/batch/reject` | 写：从 R2 删除 |

OpenAPI 描述在 `docs/api_spec_v1.json`，可直接喂给 Swagger / Redoc / Stoplight。

---

## 监控点

| 指标 | 怎么看 |
|------|--------|
| 待合并 batch 数 | `curl -s https://api.rosclaw.io/wiki/v1/batch/list \| jq '.batches \| length'` |
| 最近合并日志 | `sudo docker logs rosclaw-api --since 10m \| grep -E "Merge complete\|Seekdb reindex"` |
| SQLite 行数 | `curl -s https://api.rosclaw.io/v1/health \| jq` |
| seekdb 行数 | `sudo docker exec rosclaw-api python3 -c "from seekdb_collection_client import get_wiki_collection, get_judgments_collection; print('wiki_pages', get_wiki_collection().count()); print('judgments', get_judgments_collection().count())"` |
| R2 已归档 | 在 Cloudflare R2 dashboard 看 `submissions/processed/` |
