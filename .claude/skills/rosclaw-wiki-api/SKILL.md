---
name: rosclaw-wiki-api
description: Complete API reference for ROSClaw Wiki backend. Covers authentication, search, judgments, insights, and all frontend integration endpoints with verified curl examples.
author: ROSClaw.io
version: 1.0.0
user-invocable: true
---

# ROSClaw Wiki API — Complete Reference

**Base URL:** `https://api.rosclaw.io`

All API responses use this envelope:

```json
{"status": "ok", "data": {...}}
// or on error:
{"detail": "error message"}
```

## Authentication

### OAuth → API Key Exchange (Frontend)

```http
POST /wiki/v1/auth/exchange
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "Alice",
  "provider": "google"
}
```

**Response (new user):**

```json
{
  "status": "ok",
  "exists": false,
  "api_key": "rw_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "tenant_id": "user@example.com",
  "plan": "free",
  "created_at": "2026-05-10T12:00:00"
}
```

**Response (existing user):**

```json
{
  "status": "ok",
  "exists": true,
  "tenant_id": "user@example.com",
  "plan": "free",
  "created_at": "2026-05-10T12:00:00",
  "message": "API key already exists. Use the key stored in your browser."
}
```

**Frontend pattern:** Store `api_key` in `localStorage` under key `rosclaw_api_key`. On subsequent logins, if `exists: true`, use the stored key.

### Get Current User

```http
GET /wiki/v1/auth/me
X-API-Key: rw_sk_xxx
```

**Response:**

```json
{
  "status": "ok",
  "user": {
    "id": "user@example.com",
    "email": "user@example.com",
    "plan": "free",
    "created_at": "2026-05-10T12:00:00"
  },
  "api_key": "rw_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "api_key_masked": "rw_sk_****...****abcd",
  "usage_today": 15,
  "daily_limit": 100
}
```

### Usage Statistics

```http
GET /wiki/v1/usage?days=30
X-API-Key: rw_sk_xxx
```

**Response:**

```json
{
  "status": "ok",
  "usage": {
    "total_calls": 245,
    "total_tokens": 125000,
    "avg_latency_ms": 45.2,
    "period_days": 30,
    "by_endpoint": {
      "/v1/search": 120,
      "/v1/judgments": 45,
      "/v1/physics/impact": 30
    },
    "daily_breakdown": [
      {"date": "2026-05-10", "calls": 15},
      {"date": "2026-05-09", "calls": 42}
    ]
  }
}
```

## Public Endpoints (No Auth)

### Health Check

```http
GET /v1/health
```

```json
{"status": "ok", "backend": "sqlite_compat", "wiki_pages": 804, "judgments": 1024}
```

### Wiki Hub Stats

```http
GET /wiki/v1/hub/stats
```

**Response:**

```json
{
  "status": "ok",
  "wiki_name": "ROSClaw Wiki",
  "description": "具身智能物理常识中枢...",
  "global_stats": {
    "total_pages": 804,
    "total_wikilinks": 7650,
    "total_judgments": 1024,
    "total_code_graph_nodes": 0,
    "total_code_graph_edges": 0,
    "robots_covered": 4,
    "entities_covered": 25,
    "causal_chains": 0,
    "last_updated": "2026-05-10 00:04:49"
  },
  "keywords": [
    {"name": "Vision-Language Navigation (VLN)", "weight": 1.0, "type": "concept", "pages": 1}
  ],
  "keyword_categories": {
    "concept": [...],
    "entity": [...],
    "algorithm": [...],
    "skill": [...]
  }
}
```

## Search & Knowledge (Requires X-API-Key)

### Hybrid Search

```http
POST /v1/search
Content-Type: application/json
X-API-Key: rw_sk_xxx

{
  "query": "G1 gait control",
  "search_type": "hybrid",
  "top_k": 10
}
```

**Search types:** `keyword`, `semantic`, `hybrid`

### Get Judgments

```http
GET /v1/judgments/{entity}
X-API-Key: rw_sk_xxx
```

Example: `/v1/judgments/Unitree_G1`

Returns resolved physical parameter truths for the entity.

### Knowledge Insights

```http
GET /v1/insights
X-API-Key: rw_sk_xxx
```

Returns knowledge gap analysis — topics with low coverage or conflicting sources.

## Advanced Endpoints

### Physical Impact Chain

```http
POST /v1/physics/impact
Content-Type: application/json
X-API-Key: rw_sk_xxx

{
  "entity": "Unitree_G1",
  "parameter": "knee_torque",
  "proposed_value": "300 N·m"
}
```

### Physical Feasibility Check

```http
POST /v1/physics/feasibility
Content-Type: application/json
X-API-Key: rw_sk_xxx

{
  "code_snippet": "...",
  "target_entity": "Unitree_G1"
}
```

### Code Generation (with constraints)

```http
POST /v1/code/generate
Content-Type: application/json
X-API-Key: rw_sk_xxx

{
  "task": "Move G1 arm to pose",
  "language": "python",
  "inject_constraints": true
}
```

## Rate Limits

| Plan | Limit | Window |
|------|-------|--------|
| free | 100 | day |
| pro | 10,000 | month |
| enterprise | unlimited | — |

**Headers on every response:**

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 2026-05-11T00:00:00
```

## Error Codes

| HTTP | Meaning | Action |
|------|---------|--------|
| 400 | Bad request | Check request body/schema |
| 401 | Invalid/missing API key | Clear localStorage, re-login |
| 429 | Rate limited | Wait for reset window |
| 500 | Server error | Retry with backoff |

## Frontend Integration Quick Reference

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "https://api.rosclaw.io";
const API_KEY = typeof window !== "undefined" ? localStorage.getItem("rosclaw_api_key") : "";

async function apiGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "X-API-Key": API_KEY },
  });
  if (res.status === 401) {
    localStorage.removeItem("rosclaw_api_key");
    window.location.href = "/login";
  }
  return res.json();
}

async function apiPost(path: string, body: object) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(body),
  });
  return res.json();
}
```

## CORS Configuration

Backend allows these origins by default:

```
https://www.rosclaw.io
https://rosclaw.io
http://localhost:3000
http://localhost:5173
```

Override via `CORS_ORIGINS` env var:

```bash
CORS_ORIGINS="https://myapp.vercel.app,http://localhost:3000"
```

## Local Development Override

Create `.env.local` in your Next.js project:

```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

Backend CORS is pre-configured to allow `localhost:3000` and `localhost:5173`.
