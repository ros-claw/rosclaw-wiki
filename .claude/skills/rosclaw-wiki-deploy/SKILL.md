---
name: rosclaw-wiki-deploy
description: Deploy, operate, and troubleshoot the ROSClaw Wiki production stack (Docker Compose + Cloudflare + R2 + nginx + admin batch sync). Use when shipping backend changes, debugging the admin UI, or onboarding someone to the prod environment.
---

# ROSClaw Wiki — Production Deploy & Ops Skill

> Companion to `rosclaw-wiki-ingest` (focused on the device-side content pipeline). This skill is everything you need to operate `api.rosclaw.io` once a batch lands in R2.

## When to Invoke

- Pushing backend code (`commercial_api.py`, `batch_sync.py`, `r2_sync.py`) and need to redeploy
- Admin UI Batch Sync tab is misbehaving (Failed to fetch, Merge failed, stuck pending)
- nginx / Cloudflare / R2 / Docker Compose interaction is in question
- Onboarding someone new to the production stack

## Production Topology

```
Cloudflare (DNS + TLS termination at edge)
    ↓
host nginx (43.160.250.80:443) — /etc/nginx/sites-enabled/rosclaw
    ↓ proxy_pass http://127.0.0.1:8000
docker-compose (~ubuntu/rosclaw/rosclaw-wiki/docker-compose.prod.yml)
    ├── rosclaw-api      (python:3.11-slim, FastAPI + gunicorn-uvicorn, port 8000)
    ├── rosclaw-seekdb   (oceanbase/seekdb:latest, port 2881)
    └── rosclaw-redis    (redis:7-alpine, port 6379)
```

Production server: `ubuntu@43.160.250.80`, working directory `~/rosclaw/rosclaw-wiki`.

## One-Time Setup (new server / fresh clone)

1. Clone repo to `~/rosclaw/rosclaw-wiki`
2. Copy `.env.example` to `.env`, fill `R2_*`, `SEEKDB_*`, `REDIS_*`
3. Install Docker + Docker Compose v2
4. Ensure host nginx has `/etc/nginx/sites-enabled/rosclaw` with:
   - `upstream rosclaw_api { server 127.0.0.1:8000; }`
   - `location /wiki/v1/batch/ { proxy_pass http://rosclaw_api; proxy_read_timeout 600s; proxy_send_timeout 600s; ... }` (batch endpoints can be slow)
   - `location / { proxy_pass http://rosclaw_api; ... }` (everything else)
   - LetsEncrypt SSL for `api.rosclaw.io`
5. `sudo docker compose -f docker-compose.prod.yml up -d --build`

See `docs/DEPLOY.md` §5 for the canonical command sequence.

## Routine Operations

### Deploy backend change

```bash
ssh ubuntu@43.160.250.80
cd rosclaw/rosclaw-wiki
git pull origin main
sudo docker compose -f docker-compose.prod.yml build rosclaw-api
sudo docker compose -f docker-compose.prod.yml up -d rosclaw-api
```

Then verify:

```bash
curl -s https://api.rosclaw.io/v1/health | jq
curl -s https://api.rosclaw.io/wiki/v1/batch/list | jq
```

### Reload after wiki/ or data/ content change (no image rebuild needed)

```bash
sudo docker exec rosclaw-api kill -HUP 1
```

Why: gunicorn `preload_app=True` caches `code_graph.json` in the master and forks workers from it. `HUP` graceful-reloads workers so they re-import the changed file.

### Tail logs

```bash
sudo docker logs rosclaw-api --tail 100 -f
sudo docker logs rosclaw-api --since 10m | grep -E 'Merge|Seekdb|ERROR'
```

## Admin UI Batch Sync Diagnostics

The `/admin → Batch Sync` tab at `https://www.rosclaw.io/admin` hits four endpoints:

| UI action | Endpoint | Server function |
|-----------|----------|-----------------|
| Page load | `GET /wiki/v1/batch/list` | `r2_sync.list_submissions_detailed` (filters out `/processed/`) |
| Click row | `POST /wiki/v1/batch/preview` | downloads tarball, returns parsed `manifest.json` |
| Click Merge | `POST /wiki/v1/batch/merge` | `production_merge_from_r2(skip_seekdb=True)` then background `reindex_seekdb_from_tarball` + `move_object` |
| Click Reject | `POST /wiki/v1/batch/reject` | `r2_sync.delete_object` |

If any of these returns 5xx, look at `sudo docker logs rosclaw-api` for the Python traceback.

### Known historical bugs (don't re-introduce!)

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| `Failed to fetch batches` in UI | container's `/app/utils/r2_sync.py` lacked `list_submissions`; PYTHONPATH in `Dockerfile.prod` puts `/app/utils` before `/app`, so the utils copy shadowed the root one | keep `utils/r2_sync.py` canonical; root `r2_sync.py` mirrors it; update both together |
| `Merge failed: [Errno 30] Read-only file system: '/app/wiki/...'` | `docker-compose.prod.yml` mounted `./wiki:/app/wiki:ro` | drop the `:ro` flag — admin merges must write to host wiki/ |
| `Seekdb batch upsert failed: missing 1 required positional argument: 'ids'` | called `coll.upsert(documents=[{"id":..., "metadata":..., "embeddings":...}])` | seekdb signature is `upsert(ids=[...], documents=[...], metadatas=[...], embeddings=[...])` — parallel scalar-only lists; serialize non-scalar metadata to JSON |
| 504/502 after ~60-90s when merging a large batch | seekdb embeddings for 800+ docs blocks the response past Cloudflare/nginx upstream timeout | move the slow path to `BackgroundTasks` (`commercial_api.batch_merge`); return immediately with `seekdb_reindex: scheduled` |
| Merged batches still showing "pending" with "Invalid Date" | `batch_list` returned only keys and hard-coded `created_at: ""`; merges didn't delete the tarball | use `list_submissions_detailed`, filter `/processed/`, and `move_object` source → `submissions/processed/` after a successful merge |
| Frontend shows no feedback on merge success | `handleMerge` only `alert`ed on `!res.ok`; backend returns `{status:"error"}` with HTTP 200 too | parse JSON body, treat `status !== "ok"` as failure even on 200; alert with merge stats on success |
| Container has empty `R2_*` env vars | `sudo` strips env vars from the shell; docker-compose reads `.env` independently | put R2 vars in `.env`, reference as `${R2_ENDPOINT}` in `docker-compose.prod.yml` `environment:` block — works under sudo |
| Code change in `r2_sync.py` not picked up | `Dockerfile.prod` `COPY . .` bakes source into image | always `docker compose build rosclaw-api` after Python code changes |

## R2 Bucket Layout

```
rosclaw-wiki/
├── submissions/                              ← pending (admin UI shows these)
│   ├── batch_vln_expansion_20260511_141711.tar.gz
│   └── deepmind_20260511_043855.tar.gz
└── submissions/processed/                    ← already merged (admin UI hides these)
    ├── batch_vln_expansion_20260511_141711.tar.gz
    └── deepmind_20260511_043855.tar.gz
```

Move between prefixes via the helper:

```python
from r2_sync import move_object
move_object("submissions/processed/foo.tar.gz", "submissions/foo.tar.gz")  # un-archive to re-merge
```

## Python Version

**Production and dev use Python 3.11.** `.python-version` in repo root pins it; `pyproject.toml` enforces `requires-python = ">=3.11,<3.12"`; `Dockerfile.prod` builds from `python:3.11-slim`. Don't run scripts with system `python3` on the dev box — confirm `which python` resolves to `.venv/bin/python` first.

## Useful One-Liners

```bash
# Count pending vs processed batches
sudo docker exec rosclaw-api python3 -c '
from r2_sync import list_submissions
pending = [k for k in list_submissions("submissions") if "/processed/" not in k]
processed = [k for k in list_submissions("submissions/processed") if k.endswith(".tar.gz")]
print(f"pending: {len(pending)}, processed: {len(processed)}")'

# Check seekdb counts (often diverges from SQLite if reindex was killed)
sudo docker exec rosclaw-api python3 -c '
from seekdb_collection_client import get_wiki_collection, get_judgments_collection
print("wiki_pages:", get_wiki_collection().count())
print("judgments:", get_judgments_collection().count())'

# SQLite truth
curl -s https://api.rosclaw.io/v1/health | jq '.wiki_pages, .judgments'

# Trigger a manual seekdb reindex if background task got lost
sudo docker exec rosclaw-api python3 -c '
from batch_sync import reindex_seekdb_from_tarball
reindex_seekdb_from_tarball("/app/data/submissions/<batch>.tar.gz")'
```

## Related Docs

- `docs/DEPLOY.md` — full deploy guide (Cloudflare Tunnel, nginx, Docker Compose, R2)
- `docs/ADMIN_BATCH_SYNC.md` — end-to-end batch sync workflow with sequence diagrams
- `docs/api_spec_v1.json` — OpenAPI spec (includes `/wiki/v1/batch/*` schemas)
- `docs/ENVIRONMENT.md` — every env var and where it's read
- `~/.claude/skills/rosclaw-wiki-ingest/SKILL.md` — device-side ingestion (companion skill)
