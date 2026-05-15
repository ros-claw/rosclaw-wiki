---
name: rosclaw-wiki-dev
description: Local development setup, testing, and debugging for the ROSClaw Wiki project. Covers dependency installation, running the API, MCP server, and test suite.
author: ROSClaw.io
version: 1.0.0
user-invocable: true
---

# ROSClaw Wiki — Developer Setup & Operations

## Repository Structure

```
rosclaw-wiki/
├── commercial_api.py           # FastAPI backend (all /v1 and /wiki/v1 endpoints)
├── api/
│   ├── auth_manager.py         # API Key generation & validation
│   ├── billing_middleware.py   # Usage logging & summaries
│   └── rate_limiter.py         # Rate limiting (free/pro/enterprise plans)
├── search/
│   └── seekdb_client.py        # SQLite/SeekDB connection + schema
├── utils/
│   └── cache_client.py         # Redis primary + in-memory fallback cache
├── rosclaw_fetch.py            # Awesome List → raw downloads
├── wiki_engine.py              # Core wiki operations (frontmatter, lifecycle)
├── mcp_wiki_server.py          # MCP tools for LLM agent integration
├── knowledge_synthesizer.py    # Knowledge gap analysis
├── batch_ingest.py             # Batch processing pipeline
├── search_backend.py           # Hybrid search (BM25 + vector + graph)
├── vector_index.py             # Sentence-transformers vector store
├── entity_resolver.py          # Entity disambiguation
├── graph_exporter.py           # Graph data export
├── docker-compose.prod.yml     # Production deployment stack
├── wiki/                       # Markdown wiki (Obsidian vault)
│   ├── index.md
│   ├── log.md
│   └── {entities,algorithms,concepts,skills,episodes,archive}/
└── data/
    ├── raw/{papers,code,articles}/
    └── seekdb_compat.db        # SQLite database (auto-created)
```

## Environment Setup

### Option A: Local Python (Development)

```bash
# Python 3.11+ required
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Download sentence-transformers model (auto-cached)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
```

### Option B: Docker (Production-like)

```bash
# Full stack: API + SeekDB + Redis + Nginx
docker-compose -f docker-compose.prod.yml up -d

# Verify services
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/v1/health
```

## Running Services

### 1. FastAPI Backend

```bash
# Development (single worker, auto-reload)
python -m uvicorn commercial_api:app --host 0.0.0.0 --port 8000 --reload

# Production (multi-worker via Gunicorn)
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py commercial_api:app
```

**Environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `WIKI_ROOT` | `wiki` | Path to markdown wiki directory |
| `WIKI_BACKEND` | `seekdb` | Storage backend |
| `SEEKDB_SQLITE_PATH` | `data/seekdb_compat.db` | SQLite database path |
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `CORS_ORIGINS` | `https://www.rosclaw.io,...` | Comma-separated CORS origins |

### 2. MCP Wiki Server

```bash
# stdio transport (for Claude Desktop / Claude Code)
python mcp_wiki_server.py

# The server exposes these tools:
# wiki_ingest_source, wiki_create_page, wiki_update_page,
# wiki_supersede, wiki_auto_lint, wiki_search
```

**Claude Desktop config snippet:**

```json
{
  "mcpServers": {
    "rosclaw-wiki": {
      "command": "python",
      "args": ["/path/to/rosclaw-wiki/mcp_wiki_server.py"],
      "transportType": "stdio"
    }
  }
}
```

### 3. Batch Ingest Pipeline

```bash
# Process a directory of raw sources
python batch_ingest.py --input data/raw/papers --output wiki/entities --type paper

# Process with LLM enrichment (slower, higher quality)
python batch_ingest.py --input data/raw --llm-backend claude --workers 4
```

## Testing

### Run All Tests

```bash
pytest test_e2e.py -v
```

### Run Specific Test

```bash
pytest test_e2e.py::test_full_pipeline -v
```

### Test Coverage

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

### Manual API Test Script

```bash
BASE="http://localhost:8000"

# Health
curl "$BASE/v1/health"

# Auth exchange (new user)
curl -X POST "$BASE/wiki/v1/auth/exchange" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test", "provider": "github"}'

# Auth me (use returned API key)
curl "$BASE/wiki/v1/auth/me" -H "X-API-Key: rw_xxx"

# Search
curl -X POST "$BASE/v1/search" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: rw_xxx" \
  -d '{"query": "G1 gait", "search_type": "hybrid"}'

# Judgments
curl "$BASE/v1/judgments/Unitree_G1" -H "X-API-Key: rw_xxx"

# Insights
curl "$BASE/v1/insights" -H "X-API-Key: rw_xxx"

# Hub stats (no auth)
curl "$BASE/wiki/v1/hub/stats"
```

## Database Operations

### Inspect SQLite Schema

```bash
sqlite3 data/seekdb_compat.db ".schema"
```

### Key Tables

| Table | Purpose |
|-------|---------|
| `wiki_pages` | All wiki pages (title, body, tags, confidence, embedding) |
| `judgments` | Resolved physical parameter truths |
| `api_keys` | Tenant API keys (hashed) |
| `api_usage` | Per-endpoint usage logs |
| `entity_graph` | Typed relationships between entities |
| `wiki_pages_fts` | Full-text search virtual table (FTS5) |

### Reset Database (Caution)

```bash
rm data/seekdb_compat.db
# Auto-recreated on next API/MCP start via _ensure_schema()
```

## Debugging

### Check API Logs

```bash
# Docker
docker logs rosclaw-api --tail 50

# Local
tail -f logs/api.log
```

### Check Cache Status

```bash
# Redis
redis-cli ping
redis-cli info stats

# Test cache client
python -c "
from utils.cache_client import CacheClient
c = CacheClient()
c.set('test', 'hello', ttl=60)
print(c.get('test'))
"
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `sqlite3.OperationalError: attempt to write a readonly database` | `data/` mounted `:ro` in Docker | Remove `:ro` from docker-compose volume mount |
| `KeyError: 'created_at'` | `generate_api_key` missing field | Ensure `api/auth_manager.py` returns `created_at` |
| `Hub stats DB query failed: no such column: source` | Wrong column name in query | Use `source_entity` not `source` for `entity_graph` table |
| 429 Too Many Requests | Rate limit exceeded | Check `X-RateLimit-Remaining` header; wait for reset |
| CORS error from Vercel | Origin not in `CORS_ORIGINS` | Add `https://www.rosclaw.io` to env var |

## Development Checklist

Before committing:

- [ ] `pytest test_e2e.py` passes
- [ ] `python -m py_compile commercial_api.py` (syntax check)
- [ ] API health endpoint returns 200
- [ ] New endpoints tested with curl
- [ ] No secrets in code (use env vars)
- [ ] Frontmatter schema valid on new wiki pages

## Deployment

```bash
# Production deploy (Ubuntu server with Docker)
ssh ubuntu@api.rosclaw.io '
  cd ~/rosclaw/rosclaw-wiki
  git pull
  sudo docker stop rosclaw-api
  sudo docker rm rosclaw-api
  sudo docker-compose -f docker-compose.prod.yml up -d --no-deps --build rosclaw-api
'

# Verify
curl https://api.rosclaw.io/v1/health
curl https://api.rosclaw.io/wiki/v1/hub/stats
```
