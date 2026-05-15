# ROSClaw Wiki API Skill

> Complete reference for integrating with the ROSClaw Wiki REST API.

## Base URL

```
https://api.rosclaw.io
```

## Authentication

All endpoints require an API key passed via the `X-API-Key` header:

```bash
curl -H "X-API-Key: rw_YOUR_KEY" https://api.rosclaw.io/v1/health
```

Get your API key from https://www.rosclaw.io/profile after signing in.

---

## Endpoints

### Health Check

```http
GET /v1/health
```

Returns service status and wiki statistics.

**Response:**
```json
{
  "status": "ok",
  "wiki_pages": 6100,
  "judgments": 1024,
  "last_updated": "2026-05-14T22:50:51Z"
}
```

---

### Search

```http
POST /v1/search
Content-Type: application/json
```

Full-text and semantic search across the wiki.

**Request body:**
```json
{
  "query": "navigation",
  "search_type": "hybrid",
  "top_k": 10
}
```

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Search query |
| `search_type` | string | `keyword`, `semantic`, `hybrid`, `expanded`, `judgment` |
| `top_k` | int | Max results (default 10) |

**Response:**
```json
{
  "status": "ok",
  "query": "navigation",
  "results": [
    {
      "file_path": "huron",
      "title": "HuRoN",
      "snippet": "HuRoN is a benchmark for visual navigation...",
      "score": 1.0
    }
  ],
  "count": 6
}
```

---

### Hybrid Search

```http
POST /v1/search/hybrid
Content-Type: application/json
```

Higher-precision hybrid search with reranking.

Same request/response format as `/v1/search`.

---

### Get Judgments

```http
GET /v1/judgments/{entity}
```

Get resolved physical parameter truths for an entity.

**Example:**
```bash
curl -H "X-API-Key: rw_YOUR_KEY" \
  "https://api.rosclaw.io/v1/judgments/unitree_g1"
```

---

### Knowledge Insights

```http
GET /v1/insights
```

Get knowledge gap analysis and research suggestions.

---

### Physics Impact Analysis

```http
POST /v1/physics/impact
Content-Type: application/json
```

Trace causal ripple effects of a parameter change.

**Request body:**
```json
{
  "entity": "unitree_g1",
  "parameter": "motor_current",
  "change": "+20%"
}
```

---

### Physics Conflict Resolution

```http
POST /v1/physics/resolve
Content-Type: application/json
```

Tri-party arbitration for conflicting physical values.

---

### Topology Trace

```http
POST /v1/topology/trace
Content-Type: application/json
```

Trace causal chains through the constraint graph.

---

### Wiki Hub Stats

```http
GET /wiki/v1/hub/stats
```

Get comprehensive wiki statistics for the Hub page.

**Response includes:**
- `global_stats.total_pages`
- `global_stats.total_wikilinks`
- `global_stats.total_judgments`
- `global_stats.robots_covered`
- `keywords` — top concepts/entities/algorithms/skills
- `keyword_categories` — grouped by type

---

### Code Generation

```http
POST /v1/code/generate
Content-Type: application/json
```

Generate code skeletons with safety limits enforced.

---

### Code Sync Check

```http
POST /v1/code/sync
Content-Type: application/json
```

Check wiki-to-code parameter consistency.

---

### Batch Operations

#### List Pending Batches
```http
GET /wiki/v1/batch/list
```

#### Preview Batch
```http
POST /wiki/v1/batch/preview
Content-Type: application/json

{
  "r2_key": "submissions/batch_xxx.tar.gz"
}
```

#### Merge Batch
```http
POST /wiki/v1/batch/merge
Content-Type: application/json

{
  "r2_key": "submissions/batch_xxx.tar.gz"
}
```

#### Reject Batch
```http
POST /wiki/v1/batch/reject
Content-Type: application/json

{
  "r2_key": "submissions/batch_xxx.tar.gz"
}
```

---

## Error Codes

| Status | Meaning |
|--------|---------|
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — missing or invalid API key |
| 403 | Forbidden — rate limit exceeded |
| 404 | Not Found — endpoint or resource doesn't exist |
| 429 | Too Many Requests — slow down |
| 500 | Internal Server Error |

---

## Rate Limits

- 100 requests/minute for free tier
- 1000 requests/minute for paid tier

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1715731200
```

---

## SDK Examples

### Python

```python
import requests

API_KEY = "rw_YOUR_KEY"
BASE = "https://api.rosclaw.io"

# Search
r = requests.post(
    f"{BASE}/v1/search",
    headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    json={"query": "quadruped locomotion", "search_type": "hybrid", "top_k": 5}
)
data = r.json()
for item in data["results"]:
    print(f"{item['title']}: {item['snippet'][:100]}...")

# Get stats
r = requests.get(f"{BASE}/wiki/v1/hub/stats", headers={"X-API-Key": API_KEY})
stats = r.json()["global_stats"]
print(f"Pages: {stats['total_pages']}, Judgments: {stats['total_judgments']}")
```

### JavaScript/TypeScript

```typescript
const API_KEY = "rw_YOUR_KEY";
const BASE = "https://api.rosclaw.io";

async function searchWiki(query: string) {
  const res = await fetch(`${BASE}/v1/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify({ query, search_type: "hybrid", top_k: 10 }),
  });
  return res.json();
}
```

---

## MCP Server (Local)

For Claude Code / Cursor integration, use the MCP server:

```bash
python mcp_wiki_server.py --wiki-root ./wiki
```

**17 tools available:**
- `auto_ingest` — automatic source ingestion
- `wiki_create_page` / `wiki_update_page` / `wiki_delete_page` — CRUD
- `wiki_read_page` — read page content
- `wiki_list_pages` / `wiki_search_by_tag` — discovery
- `wiki_supersede` — page lifecycle
- `wiki_auto_lint` — quality checks
- `search_wiki` — full-text/semantic search
- `find_orphan_pages` — find unlinked pages
- `retention_decay` / `retention_suggest_archival` — knowledge metabolism
- `wiki_export_graph` — graph export
- `wiki_consolidate` — merge fragments
- `qa_ask` — RAG Q&A
- `wiki_get_stats` — wiki statistics

---

## Links

- Web UI: https://www.rosclaw.io/hub/wiki
- Admin: https://www.rosclaw.io/admin
- Profile (API Key): https://www.rosclaw.io/profile
