# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ROSClaw Wiki is a knowledge management system for embodied AI and robotics. It transforms raw sources (papers, code, URDFs) into a structured, queryable wiki with causal physical reasoning. It serves as a "physical commonsense firewall" — tracing how a parameter change (e.g., increasing motor current) ripples through a system (heat → drift → failure).

The system has four public interfaces:
- **REST API** (`commercial_api.py`) — hosted at `api.rosclaw.io` (FastAPI + Gunicorn)
- **Wiki Web UI** (`web_ui/app.py`) — hosted at `wiki.rosclaw.io` (Flask + SocketIO + Sigma.js)
- **MCP Server** (`mcp_wiki_server.py`) — integrates with Claude Code / OpenClaw
- **CLI** (`rosclaw_wiki/cli.py`) — local knowledge forging and cloud push

## Development Commands

Install dependencies:
```bash
pip install -r requirements.txt          # base deps
pip install -e ".[dev]"                  # with pytest, ruff, mypy
```

Lint and type check:
```bash
ruff check .                             # lint (config in pyproject.toml)
ruff format .                            # format
mypy                                     # type check
```

Run the API server (dev):
```bash
uvicorn commercial_api:app --reload
```

Run the Wiki Web UI (dev):
```bash
python -m web_ui.app                     # Flask on port 5000
```

Run the MCP server:
```bash
python mcp_wiki_server.py --wiki-root ./wiki
```

Run the knowledge pipeline:
```bash
bash scripts/local_processing_pipeline.sh        # full 7-step forge pipeline
python utils/workflow_orchestrator.py --run-all  # event-driven one-shot
python utils/workflow_orchestrator.py --watch    # event-driven daemon
python ingest/batch_ingest.py                    # ingest raw sources only
```

CLI usage:
```bash
rosclaw-wiki forge --input ./papers --name "my-wiki"
rosclaw-wiki push --name "my-wiki"
```

Note: there are currently **no test files** in `tests/` (only an empty `__init__.py`). Tests existed in earlier phases but were removed during the package restructuring.

## Architecture

### Package Layout

Modules are grouped by functional domain under subdirectories. Root-level entry points (`commercial_api.py`, `mcp_wiki_server.py`) insert subdirectories into `sys.path` at runtime so modules can be imported flat (e.g., `import wiki_engine` not `from core import wiki_engine`).

| Package | Contents |
|---------|----------|
| `api/` | API key validation, billing middleware, rate limiting |
| `code/` | Code generator, code knowledge graph, repo scanner, PR generator, tree-sitter parser |
| `core/` | Wiki engine, storage interface, wiki hub, event bus, file lock, SeekDB export |
| `dream/` | Dream cycle, dream sandbox |
| `ingest/` | Batch ingest, PDF extraction, fetch, URDF import, multimodal extraction, OCR |
| `knowledge/` | Judgment generator, conflict resolver, entity linker/resolver, synthesizer, ontology, physics grounding, QA, retention, context router |
| `robot/` | Constraint graph (causal physical reasoning) |
| `search/` | Whoosh backend, vector index, search interface, SeekDB clients, page indexer |
| `utils/` | LLM interface, GitHub gateway, graph exporter, scheduler, workflow orchestrator, R2 sync, research advisor |
| `web_ui/` | Flask + SocketIO frontend app and Sigma.js visualization |
| `scripts/` | One-off setup, seeding, and utility scripts |

### Wiki Storage Model

Knowledge is stored as Markdown files with YAML frontmatter in `wiki/`. Every page has `id`, `type`, `tags`, `confidence`, `created_at`, `last_reinforced`, `sources`, and `supersedes`. Internal links use `[[Wikilink]]` syntax.

| Directory | Content |
|-----------|---------|
| `wiki/entities/` | Robots, sensors, hardware platforms |
| `wiki/algorithms/` | Control algorithms, neural nets, VLA models, SLAM |
| `wiki/concepts/` | Theory, frameworks, taxonomies |
| `wiki/skills/` | Executable procedures, ROS nodes, MCP tool descriptions |
| `wiki/episodes/` | Raw session notes, single-source summaries |
| `wiki/judgments/` | Resolved parameter truths for entities |
| `wiki/index.md` | Auto-generated catalog |
| `wiki/log.md` | Append-only operation log |

Core wiki I/O lives in `core/wiki_engine.py` (`parse_frontmatter`, `write_frontmatter`, `generate_page_id`).

### Knowledge Pipeline (Ingestion)

There are two pipeline modes:

**Batch pipeline** (`scripts/local_processing_pipeline.sh`) — the 7-step forge pipeline run on local infrastructure:
1. Fetch sources (`ingest/rosclaw_fetch.py` from `awesome_vln.yml`)
2. PDF full-text extraction (`ingest/pdf_extractor.py`)
3. Batch ingest into wiki (`ingest/batch_ingest.py`)
4. Build code knowledge graph (`code/code_knowledge_graph.py`)
5. Auto-judgment pipeline (`knowledge/auto_judgment_pipeline.py`)
6. Causal chain extraction (`ingest/autonomous_extractor.py`)
7. Build physical ontology and export (`robot/constraint_graph.py` → `data/seekdb_import.jsonl`)

**Event-driven pipeline** (`utils/workflow_orchestrator.py`) — chains stages reactively via the event bus:
```
raw_watcher_alert → batch_ingest → entity_linker → conflict_resolver → judgment_generator
```

Stages communicate through `core/event_bus.py`, a JSONL-based cross-process event log at `data/events.jsonl`.

LLM calls go through `utils/llm_interface.py`, which auto-detects the backend from env vars (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`). Set `ROSCLAW_MOCK_LLM=1` to use the mock backend for testing.

### Physical Reasoning (The "Firewall")

The causal reasoning engine lives in `robot/constraint_graph.py` and `knowledge/physical_ontology.py`:

- **Tri-party arbitration** (`robot/constraint_graph.py:tri_party_arbitration`) resolves conflicting physical values from URDF (weight 1.0), code (0.8), and papers (0.6)
- **Impact chain analysis** performs BFS radius-3 traversal of the constraint graph to trace causal ripple effects
- **Physics grounding** (`knowledge/physics_grounding.py`) scans code for physical constants (AST + regex) and links them to wiki judgments via `CONSTRAINT_BY` edges
- **Context switching** supports `simulation` vs `real_world` modes

### Search Stack

- **Full-text**: Whoosh (`search/search_backend.py`) with incremental indexing
- **Semantic**: `search/vector_index.py` via sentence-transformers
- **Hybrid**: `search/search_interface.py` combines both; supports `keyword` | `semantic` | `hybrid` | `expanded` | `judgment` search types
- **QA**: `knowledge/qa_engine.py` retrieval-augmented QA over the wiki

Upper-layer code must use `SearchInterface` (ABC in `search/search_interface.py`), not backend modules directly.

### Storage Backends

The system abstracts storage via `StorageInterface` (ABC in `core/storage_interface.py`):

- **Filesystem** (default) — markdown files + whoosh index
- **SQLite** — `search/seekdb_client.py` provides a compatibility layer at `data/seekdb_compat.db`
- **SeekDB** (production) — OceanBase/SeekDB cluster, configured via `SEEKDB_HOST`/`SEEKDB_PORT`

Select backend via `WIKI_BACKEND=seekdb` env var.

### Code Knowledge Graph

`code/code_repo_scanner.py` + `code/code_knowledge_graph.py` parse ROS/robotics codebases using tree-sitter, extracting:
- Physical constants (torque limits, safety thresholds)
- Topic publishers/subscribers
- URDF links and joints

`ingest/urdf_importer.py` parses URDF files into the physical ontology. `utils/github_gateway.py` fetches repos for analysis.

### Cloud / Commercial API

`commercial_api.py` exposes FastAPI endpoints with:
- `api/auth_manager.py` — API key validation
- `api/billing_middleware.py` — usage tracking
- `api/rate_limiter.py` — per-tenant rate limits
- `utils/r2_sync.py` — Cloudflare R2 (S3-compatible) for file uploads

Production deploys via `docker-compose.prod.yml` (SeekDB + API + nginx + certbot). See `docs/DEPLOY.md` for full deployment instructions.

### Wiki Web UI

`web_ui/app.py` is a Flask + SocketIO application serving a Sigma.js frontend:
- REST endpoints: `/api/graph`, `/api/stats`, `/api/search`
- WebSocket push for real-time events (ingest progress, conflict alerts)
- Frontend: `web_ui/index.html` (single-page Sigma.js visualization)

### Knowledge Metabolism (Background Jobs)

Three subsystems run autonomously to keep knowledge healthy:

- **Scheduler** (`utils/scheduler.py`) — tiered background metabolism:
  - `raw_watcher` (1–8h): scans `data/raw/` for new files, emits alerts
  - `daily_review` (daily): confidence decay, orphan detection
  - `weekly_deep_scan` (weekly): stale page archival suggestions

- **Retention Engine** (`knowledge/retention_engine.py`) — confidence decay following Ebbinghaus rules:
  - 30–89 days → ×0.9
  - 90–179 days → ×0.7
  - ≥180 days → ×0.5

- **Dream Cycle** (`dream/dream_cycle.py`) — nightly autonomous thinking:
  1. Repair & Merge: fix broken wikilinks, merge fragment pages
  2. Knowledge Reinforcement: search for new sources to boost low-confidence pages
  3. Forward Insight: analyze knowledge gaps, generate research suggestions

### Safety-Critical Subsystems

- **Code Generator** (`code/code_generator.py`) — generates code skeletons with strict limits: never generates full control loops, always includes an `AUTO-GENERATED` warning header, always cites physical parameter sources, and **refuses** to generate if unresolved conflicts exist for parameters.

- **PR Generator** (`code/pr_generator.py`) — auto-generates PRs from wiki-to-code sync checks with GREEN/AMBER/RED safety labels:
  - GREEN: parameter < 80% of hardware limit → auto-merge eligible
  - AMBER: parameter ≥ 80% but < 100% → needs human review
  - RED: parameter ≥ 100% of limit → blocked with `[!CRITICAL]` report

- **Context Router** (`knowledge/context_router.py`) — routes natural-language scenarios (e.g., "G1 slips on wet ground") to the most relevant judgments and wiki pages, inferring operational context from keywords.

### Wiki Hub (Distribution)

`core/wiki_hub.py` implements a Git-friendly pack format for knowledge distribution:
- `wiki_pack()`: bundle pages, judgments, and entity relations into a versioned pack
- `wiki_unpack()`: merge a pack into a target wiki
- `wiki_diff()`: compare two packs or a pack vs local wiki
- The CLI `forge`/`push` commands use this pack format for cloud upload.

### Batch Sync (R2-based Submission Workflow)

`batch_sync.py` manages device-to-production knowledge submissions via Cloudflare R2:
- `device-package`: pack local wiki changes into a tar.gz
- `device-upload`: upload to R2 under a prefix
- `production-merge`: download from R2 and merge into production wiki

## Key Conventions

- All datetime fields use ISO 8601 format (`YYYY-MM-DD` or full ISO)
- Confidence scores are 0.0–1.0 floats; initial values depend on source type (official docs = 0.9, peer-reviewed = 0.8, blog = 0.5)
- Never modify files under `data/raw/` — they are immutable source of truth
- Never silently overwrite conflicting data; always log in `### 待核实冲突` section
- All wiki pages must have YAML frontmatter and be Obsidian-compatible
- After every ingest: update `wiki/index.md` and append to `wiki/log.md`
- Upper-layer code must use `StorageInterface` and `SearchInterface` abstractions, not backend modules directly
- See `AGENTS.md` for the full agent constitution covering ingest rules, page format, linking rules, and maintenance cadence

## Environment Variables

See `.env.example` for the full list. Key ones:
- `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` — LLM backend (at least one required for forging)
- `ROSCLAW_API_KEY` — for cloud API access / push
- `WIKI_ROOT` — path to wiki directory (default `./wiki`)
- `WIKI_BACKEND` — `filesystem` or `seekdb`
- `SEEKDB_HOST` / `SEEKDB_PORT` — SeekDB connection
- `ROSCLAW_MOCK_LLM=1` — use mock LLM for testing
- `R2_ENDPOINT` / `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` / `R2_BUCKET` — Cloudflare R2 storage
