# Environment Variables

> 生产 / 开发 / 设备端三种角色用到的所有变量，按角色分组。`.env.example`（仓库根目录）维护着一份可复制的模板，本文件解释每个变量在哪些代码路径里被读到、缺了会怎样。

## 全局 / Wiki 后端

| 变量 | 默认 | 必填？ | 用途 |
|------|------|--------|------|
| `WIKI_ROOT` | `wiki` | ✅（生产） | Markdown 库的根目录。容器内固定 `/app/wiki`。`commercial_api.py`、`batch_sync.py`、`wiki_engine.py` 都依赖。 |
| `WIKI_BACKEND` | `seekdb` | ✅（生产） | `commercial_api.startup` 据此选 `SeekDBSearchImpl`；改成 `whoosh` 走纯本地全文索引（无需 seekdb 容器，开发环境用）。 |
| `CORS_ORIGINS` | `*` | 可选 | 逗号分隔。设成 `https://www.rosclaw.io,https://rosclaw.io` 收紧前端域。 |

## seekdb（向量库）

| 变量 | 默认 | 必填？ | 用途 |
|------|------|--------|------|
| `SEEKDB_MODE` | `server` | ✅ | `server` = 通过 TCP 连 `oceanbase/seekdb` 容器；`embedded` = 进程内（不推荐生产）。 |
| `SEEKDB_HOST` | `seekdb` | ✅（server 模式） | docker compose 内部 service name；裸跑改 `127.0.0.1`。 |
| `SEEKDB_PORT` | `2881` | ✅ | seekdb 容器暴露端口。 |

## Redis（任务队列 / 缓存）

| 变量 | 默认 | 必填？ | 用途 |
|------|------|--------|------|
| `REDIS_HOST` | `redis` | ✅ | docker compose service name；裸跑改 `127.0.0.1`。 |
| `REDIS_PORT` | `6379` | ✅ | — |
| `REDIS_DB` | `0` | 可选 | 多实例隔离时分库。 |

## Cloudflare R2（设备 ⇄ admin batch sync）

| 变量 | 必填？ | 用途 |
|------|--------|------|
| `R2_ENDPOINT` | ✅ | `https://<account-id>.r2.cloudflarestorage.com`。`utils/r2_sync._get_r2_client` 拿不到会抛 `RuntimeError`。 |
| `R2_ACCESS_KEY_ID` | ✅ | R2 API token 的 access key。 |
| `R2_SECRET_ACCESS_KEY` | ✅ | 对应 secret。 |
| `R2_BUCKET` | ✅（默认 `rosclaw-wiki`） | 桶名。 |

> ⚠️ 永远不要把这些值写进任何 committed 文件。`.gitignore` 已经覆盖 `.env`，但仍要小心 docker-compose / shell history。如怀疑泄露，立刻去 Cloudflare dashboard rotate token。

## 设备端（除了 R2 之外还要）

| 变量 | 默认 | 用途 |
|------|------|------|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | — | `knowledge_synthesizer.py` 在做实体抽取 / 摘要时按需调 LLM。本地 forge 流程必填一个。 |
| `ROSCLAW_API_KEY` | — | 调 `https://api.rosclaw.io/v1/search` 等需要鉴权的端点时。 |

## 何时哪个变量被读

| 代码路径 | 读到的变量 |
|----------|-----------|
| `commercial_api.startup` | `WIKI_ROOT`、`WIKI_BACKEND` |
| `commercial_api.batch_*` 端点 | 经由 `r2_sync.*` 间接读 `R2_*` |
| `batch_sync.production_merge_from_r2` | `R2_*` |
| `batch_sync.device_upload` (设备端 CLI) | `R2_*` |
| `seekdb_collection_client._connect()` | `SEEKDB_*` |
| `redis` 客户端（任务队列） | `REDIS_*` |

## 校验

容器启动后做一次 sanity check：

```bash
sudo docker exec rosclaw-api env | grep -E '^(R2_|SEEKDB_|REDIS_|WIKI_)' | sed 's/=.*/=***/g'
```

如果 `R2_*` 全空，是 `.env` 缺失或 docker compose 启动时没读到（`sudo` 不带 `-E` 不会污染 docker，但 `docker compose` 自己读 `.env`，所以一般要么 `.env` 没填、要么 docker-compose.prod.yml 里漏了对应的 `environment:` 行）。
