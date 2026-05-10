---
name: rosclaw-wiki
description: >
  The ROSClaw Wiki knowledge engine for embodied intelligence.
  Converts GitHub Awesome Lists and repositories into structured,
  interlinked markdown wikis with physical constraint graphs.
  Also exposes a FastAPI backend with search, judgments, insights,
  and OAuth-to-API-Key authentication for Vercel frontends.
author: ROSClaw.io
version: 1.1.0
license: MIT
homepage: https://rosclaw.io
user-invocable: true
metadata:
  openclaw:
    emoji: "🗿"
    os: ["darwin", "linux", "win32"]
    requires:
      env: ["ANTHROPIC_API_KEY"]
      config: ["rosclaw-wiki"]
---

# ROSClaw Wiki — Skill Index

This repository contains **three actionable Claude Code skills** under `.claude/skills/`.
When working in this project, Claude Code automatically loads them.

## Available Skills

### 1. `rosclaw-wiki-ingest` — Knowledge Ingestion

**When to use:**
- Converting a GitHub Awesome List into wiki pages
- Distilling a single repository (paper code, robot SDK) into the knowledge base
- Batch-ingesting papers, code, or articles

**Key capabilities:**
- `rosclaw_fetch.py` → downloads arXiv PDFs, clones repos, converts articles to markdown
- `wiki_engine.py` → creates pages with YAML frontmatter, handles conflicts & supersession
- `mcp_wiki_server.py` → MCP tools: `wiki_ingest_source`, `wiki_create_page`, `wiki_auto_lint`

**Quick start:**
```bash
python rosclaw_fetch.py --input awesome.md --output-dir data/raw
python mcp_wiki_server.py
# Then use MCP tools to extract entities and create wiki pages
```

See: `.claude/skills/rosclaw-wiki-ingest/SKILL.md`

---

### 2. `rosclaw-wiki-dev` — Developer Setup & Operations

**When to use:**
- First time setting up the project locally
- Running the API, MCP server, or batch pipeline
- Debugging database, cache, or deployment issues

**Key capabilities:**
- Local Python setup vs Docker production stack
- Running FastAPI (`uvicorn`) and Gunicorn multi-worker
- Database schema, SQLite operations, reset procedures
- 6 common issues with fixes (read-only DB, missing columns, CORS, etc.)

**Quick start:**
```bash
pip install -r requirements.txt && pip install -e .
python -m uvicorn commercial_api:app --reload
```

See: `.claude/skills/rosclaw-wiki-dev/SKILL.md`

---

### 3. `rosclaw-wiki-api` — API Reference & Frontend Integration

**When to use:**
- Building a frontend that calls the ROSClaw Wiki API
- Testing endpoints or debugging auth flows
- Understanding rate limits, CORS, or error handling

**Key capabilities:**
- Complete endpoint reference with verified `curl` examples
- OAuth → API Key exchange flow for NextAuth.js / Vercel
- Rate limits: free (100/day), pro (10k/month), enterprise (unlimited)
- Frontend TypeScript snippet for authenticated requests

**Quick test:**
```bash
curl https://api.rosclaw.io/v1/health
curl https://api.rosclaw.io/wiki/v1/hub/stats
```

See: `.claude/skills/rosclaw-wiki-api/SKILL.md`

---

## Architecture Overview

```
Awesome List / GitHub Repo
       │
       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ rosclaw_fetch.py│ ──► │ wiki_engine.py  │ ──► │   wiki/*.md     │
│  (download raw) │     │ (create/update) │     │ (Obsidian vault)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                       │
       ▼                       ▼
  data/raw/               mcp_wiki_server.py
  {papers,code,articles}  (MCP tools for LLM agents)

       │
       ▼
┌─────────────────┐     ┌─────────────────┐
│ commercial_api  │ ◄── │  Vercel Frontend│
│ (FastAPI +      │     │  (Next.js +     │
│  SQLite/Redis)  │     │   NextAuth.js)  │
└─────────────────┘     └─────────────────┘
```

## Core Files

| File | Purpose |
|------|---------|
| `commercial_api.py` | FastAPI backend — all `/v1` and `/wiki/v1` endpoints |
| `api/auth_manager.py` | API Key generation, validation, rate limits |
| `api/billing_middleware.py` | Usage logging & summary queries |
| `search/seekdb_client.py` | SQLite/SeekDB connection & schema management |
| `utils/cache_client.py` | Redis primary + in-memory fallback cache |
| `wiki_engine.py` | Frontmatter parsing, confidence lifecycle, conflict handling |
| `mcp_wiki_server.py` | MCP server exposing wiki maintenance tools |
| `rosclaw_fetch.py` | Downloads raw sources from Awesome Lists |

## Philosophy

**Action is Sovereignty. Connection is Intelligence.**

We don't just store parameters; we curate the laws of the physical universe
for the machines that live in it. Every paper ingested deepens the causal graph;
every code repository scanned reveals new constraints.

## Installation

```bash
git clone https://github.com/ros-claw/rosclaw-wiki.git
cd rosclaw-wiki
pip install -r requirements.txt
pip install -e .
```

For full developer setup: see `.claude/skills/rosclaw-wiki-dev/SKILL.md`
