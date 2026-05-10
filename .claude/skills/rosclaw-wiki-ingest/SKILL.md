---
name: rosclaw-wiki-ingest
description: Ingest GitHub Awesome Lists and standalone repositories into the ROSClaw Wiki knowledge base. Handles fetching, entity extraction, page creation, conflict resolution, and index maintenance.
author: ROSClaw.io
version: 1.0.0
user-invocable: true
---

# ROSClaw Wiki Ingest — Awesome List & Repository Alchemy

## When to Use

- User has a GitHub Awesome List (e.g., `awesome-robotics`, `awesome-embodied-ai`) they want to convert into a structured wiki.
- User has a standalone GitHub repository (paper code, robot SDK) they want to distill into wiki pages.
- User wants to batch-ingest multiple sources into the ROSClaw Wiki.

## Prerequisites

```bash
# 1. Clone and enter the project
git clone https://github.com/ros-claw/rosclaw-wiki.git
cd rosclaw-wiki

# 2. Install dependencies
pip install -r requirements.txt
pip install -e .

# 3. Verify wiki directory exists
mkdir -p wiki/{entities,algorithms,concepts,skills,episodes,archive}
```

## Workflow Overview

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
```

## Step 1: Fetch Raw Sources

### 1.1 Awesome List → Raw Downloads

Create an `awesome.md` file (or use an existing one):

```bash
python rosclaw_fetch.py --input awesome.md --output-dir data/raw
```

**What it does:**
- `arxiv.org` links → PDFs in `data/raw/papers/{arxiv_id}.pdf` + JSON metadata sidecar
- `github.com` links → shallow clones in `data/raw/code/{repo_name}/` + README.md copied
- Other URLs → Markdown in `data/raw/articles/{slug}.md` via `html2text`

**Deduplication:** Checks existing files by name before downloading.

### 1.2 Single GitHub Repository

For a standalone repo (no Awesome List):

```bash
# Manual approach
cd data/raw/code
git clone --depth=1 https://github.com/org/repo.git
cd ../../..
```

Then proceed to Step 2.

## Step 2: Extract Entities & Create Wiki Pages

### 2.1 Using MCP Tools (Recommended)

Start the MCP server:

```bash
python mcp_wiki_server.py
```

Then use these tools via Claude Code / Claude Desktop:

| Tool | Purpose | Input |
|------|---------|-------|
| `wiki_ingest_source` | Read a raw file and extract entities | `source_path`, `source_type` |
| `wiki_create_page` | Create a new wiki page | `type`, `title`, `content`, `meta` |
| `wiki_update_page` | Update existing page with new info | `path`, `instruction` |
| `wiki_supersede` | Archive old page, link to new | `old_path`, `new_path` |
| `wiki_auto_lint` | Flag low-confidence/orphan pages | — |
| `wiki_search` | Search across all pages | `query` |

### 2.2 Ingest a Paper (Example)

```python
# Inside MCP session or script
wiki_ingest_source(
    source_path="data/raw/papers/2301.12345.pdf",
    source_type="paper"
)
```

**Expected behavior:**
1. Reads PDF content
2. Constructs LLM prompt for entity extraction (robots, algorithms, concepts)
3. Returns prompt string — caller runs LLM, feeds result back
4. Creates/updates wiki pages with proper frontmatter
5. Appends entry to `wiki/log.md`

### 2.3 Ingest a Code Repository (Example)

```python
wiki_ingest_source(
    source_path="data/raw/code/repo-name/README.md",
    source_type="code"
)
```

**What gets extracted:**
- Robot entities (from URDF, config files)
- Algorithms (from main modules)
- Skills (from example scripts)
- Concepts (from documentation)

## Step 3: Maintain the Wiki

### 3.1 Update Index

```python
# Rebuild wiki/index.md with all pages categorized
from wiki_engine import update_index
update_index("wiki")
```

### 3.2 Run Auto-Lint

```python
# Flag pages with confidence < 0.3 or no inbound wikilinks
wiki_auto_lint()
```

### 3.3 Handle Conflicts

When two sources disagree on a parameter:

```python
from wiki_engine import handle_conflict

updated_content = handle_conflict(
    existing_path="wiki/entities/Unitree_G1.md",
    field="max_knee_torque",
    old_val="237 N·m",
    new_val="250 N·m",
    new_source="paper:arxiv:2305.67890"
)
```

This appends a conflict record to the page's `### 待核实冲突` section.

## Step 4: Verify in Obsidian

```bash
# Open wiki folder in Obsidian
# Graph View should show:
# - Nodes: entities, algorithms, concepts, skills
# - Edges: wikilinks [[Page Title]]
# - Colors: by type (entity=blue, concept=cyan, algorithm=green, etc.)
```

## Confidence & Lifecycle Rules

### Initial Confidence by Source Type

| Source Type | Initial Confidence | Reason |
|-------------|-------------------|--------|
| Official documentation / URDF | 0.9 | Authoritative |
| Peer-reviewed paper | 0.8 | Verified |
| Blog post / tutorial | 0.5 | Subjective |
| Code comment / README | 0.6 | Implementation truth |

### Confidence Decay (Ebbinghaus)

```python
from wiki_engine import update_confidence

# Without reinforcement:
# 30 days → ×0.9
# 90 days → ×0.7
# 180 days → ×0.5

# With reinforcement (user validates):
update_confidence(meta, reinforcement=True)  # +0.05, cap 1.0
```

### Supersession Rules

Newer source + higher/equal rank → supersede old claim:

```python
from wiki_engine import check_supersession_needed

should_supersede = check_supersession_needed(new_meta, existing_meta)
```

## Frontmatter Schema

Every wiki page MUST have this YAML frontmatter:

```yaml
---
id: unitree_g1
type: entity  # entity | algorithm | concept | skill | episode
tags: [humanoid, unitree, torque]
confidence: 0.92
created_at: "2026-05-10"
last_reinforced: "2026-05-10"
supersedes: wiki/archive/Unitree_G1_v1.md  # optional
sources:
  - type: paper
    url: https://arxiv.org/abs/2301.12345
    confidence: 0.8
  - type: official
    url: https://unitree.com/g1/specs
    confidence: 0.9
---
```

## File Organization

```
wiki/
├── index.md              # Human-readable catalog
├── log.md                # Append-only chronological record
├── entities/             # Robots, hardware, datasets
├── algorithms/           # Methods, models, architectures
├── concepts/             # Theories, paradigms, metrics
├── skills/               # How-to guides, procedures
├── episodes/             # Specific experiments, results
└── archive/              # Superseded pages (with redirect stubs)
```

## Common Pitfalls

1. **Never mutate `data/raw/`** — Raw sources are immutable. All derived content goes in `wiki/`.
2. **Always check for existing pages** before creating — use `wiki_search()` or check `wiki/index.md`.
3. **Preserve conflicts** — Do not silently overwrite. Use `handle_conflict()` to document disagreements.
4. **Link aggressively** — Every page should have `[[wikilinks]]` to related pages. Unlinked pages are orphans.
5. **Validate frontmatter** — Missing `id`, `type`, or `confidence` breaks the lint check.

## Quick Start Template

```bash
# 1. Fetch
python rosclaw_fetch.py --input my_awesome.md --output-dir data/raw

# 2. Start MCP server (in one terminal)
python mcp_wiki_server.py

# 3. Ingest sources (via Claude Code with MCP)
# "Ingest all papers from data/raw/papers/ into the wiki"

# 4. Lint
python -c "from mcp_wiki_server import wiki_auto_lint; wiki_auto_lint()"

# 5. Open in Obsidian
open wiki/  # or Obsidian → Open folder as vault
```
