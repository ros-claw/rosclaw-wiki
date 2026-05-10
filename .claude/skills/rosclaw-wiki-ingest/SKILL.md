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
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│ rosclaw_fetch.py│ ──► │  CONTENT EXTRACTION │ ──► │   wiki/*.md     │
│  (download raw) │     │  (LLM-powered)      │     │ (Obsidian vault)│
└─────────────────┘     └─────────────────────┘     └─────────────────┘
       │                         │
       ▼                         ▼
  data/raw/               Knowledge Graph:
  {papers,code,articles}  entities, algorithms,
                          concepts, wikilinks,
                          judgments, causal chains
```

**CRITICAL: This is NOT a structure converter. It is a knowledge extractor.**
The agent MUST NOT stop at "I generated Markdown files." The agent MUST
continue until actual content has been parsed, entities extracted, and
relationships established via `[[wikilinks]]`.

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

## Step 2: Extract Knowledge (MANDATORY — NOT OPTIONAL)

### ⚠️ ANTI-SHORTCUT RULES

The following behaviors are **PROHIBITED** and indicate failure:

| Prohibited Behavior | Why It Fails | Correct Alternative |
|--------------------|-------------|---------------------|
| Only parsing README links into Markdown shells | No content extracted, no knowledge created | Download PDF/code, then run LLM extraction |
| Creating pages with empty or placeholder bodies | "TBD", "TODO", or one-line descriptions | Each page MUST contain extracted Methods, Results, Parameters, or API docs |
| Skipping LLM entity extraction | No entities, no relationships, no graph | MUST call LLM for every paper and every significant code repo |
| Skipping `[[wikilinks]]` | Pages are orphaned, graph is disconnected | Every page MUST link to at least 2 related pages |
| Assigning confidence = 1.0 without justification | Fake confidence, useless for reasoning | Use source-type table below |

### 2.1 Mandatory Checkpoints

Before marking any item "done", verify:

- [ ] **Content downloaded** — PDF is in `data/raw/papers/`, code is in `data/raw/code/`, or article is in `data/raw/articles/`
- [ ] **Content read** — Agent has actually read the full text (not just the title/URL)
- [ ] **LLM extraction performed** — At minimum: entities, methods, key findings, parameters
- [ ] **Page body > 200 words** — No stubs. Real extracted content.
- [ ] **Frontmatter complete** — `id`, `type`, `tags`, `confidence`, `sources` all populated
- [ ] **Wikilinks present** — `[[Related Page]]` in the body linking to other wiki pages
- [ ] **Logged** — Entry appended to `wiki/log.md`

### 2.2 Using MCP Tools

Start the MCP server:

```bash
python mcp_wiki_server.py
```

Tools:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `wiki_ingest_source` | Read raw file → construct LLM prompt → create pages | **Primary tool for every source** |
| `wiki_create_page` | Direct page creation | When you already have extracted content |
| `wiki_update_page` | Add new findings to existing page | When source provides additional data |
| `wiki_supersede` | Archive outdated page | When new source contradicts old |
| `wiki_auto_lint` | Find orphans and low-confidence pages | After batch ingest completes |
| `wiki_search` | Check if page already exists | Before creating any new page |

### 2.3 Ingest a Paper (Full Flow)

**Step A — Download (if not already in data/raw/papers/)**

```bash
# Use arxiv library or direct download
python -c "import arxiv; arxiv.Client().download(arxiv.Search(id_list=['2301.12345']).results().__next__(), dirpath='data/raw/papers')"
```

**Step B — Extract Full Text**

```python
import fitz  # PyMuPDF — already in requirements.txt

doc = fitz.open("data/raw/papers/2301.12345.pdf")
full_text = "\n".join(page.get_text() for page in doc)

# Fallback: if text is too short, the PDF may be scanned images
if len(full_text.strip()) < 500:
    # Install: pip install paddlepaddle paddleocr
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        result = ocr.ocr(pix.tobytes(), cls=True)
        # Extract text from OCR result...
```

**Why two tools?**
- **PyMuPDF** = fast, accurate for text-based PDFs (99% of arXiv papers)
- **PaddleOCR** = needed only for scanned/image-based pages
- Try PyMuPDF first. Fall back to PaddleOCR only when extracted text is insufficient.

**Step C — LLM Entity Extraction (MANDATORY)**

Construct and run this prompt:

```
You are a knowledge extraction engine for embodied intelligence research.

Read the following paper and extract:
1. **Robot entities** mentioned (name, manufacturer, DOF, key specs)
2. **Algorithms** proposed (name, architecture, input/output, metrics)
3. **Concepts** introduced (theoretical frameworks, metrics, paradigms)
4. **Skills** demonstrated (procedures, evaluation methods)
5. **Physical parameters** with values and units (torque, velocity, accuracy, etc.)
6. **Causal claims** (X causes Y, A depends on B)
7. **Relationships** between entities (uses, improves, contradicts, extends)

For each entity, provide:
- name
- type (entity|algorithm|concept|skill)
- confidence (0.0-1.0 based on evidence strength)
- source_location (section in paper)

Paper text:
---
{full_text[:8000]}  # First 8000 chars, or chunked
---
```

**Step D — Create Wiki Pages from LLM Output**

```python
from wiki_engine import create_page

for entity in llm_output["entities"]:
    create_page(
        dir=f"wiki/{entity['type']}s",
        title=entity["name"],
        body=entity["description"] + "\n\n" + entity.get("methods", ""),
        meta={
            "id": entity["name"].lower().replace(" ", "_"),
            "type": entity["type"],
            "tags": entity.get("tags", []),
            "confidence": entity["confidence"],
            "sources": [{"type": "paper", "url": f"https://arxiv.org/abs/{arxiv_id}", "confidence": 0.8}],
        }
    )
```

**Step E — Link Pages**

Edit each new page to add `[[wikilinks]]` to related pages:

```markdown
This algorithm [[EfficientNav]] improves upon [[Vision-Language Navigation (VLN)]]
by introducing [[Spatial Intelligence in Navigation]].
```

### 2.4 Ingest a Code Repository (Full Flow)

**Step A — Clone**

```bash
cd data/raw/code
git clone --depth=1 https://github.com/org/repo.git
cd ../../..
```

**Step B — Read Code Structure**

```python
import os

repo_path = "data/raw/code/repo"
# Read main module files, README, and config files
for root, dirs, files in os.walk(repo_path):
    for f in files:
        if f.endswith((".py", ".cpp", ".h", ".yaml", ".urdf", ".md")):
            # Read and summarize
            pass
```

**Step C — LLM Extraction**

```
Analyze the following code repository for embodied intelligence:

README:
{readme_text}

Main module:
{main_code}

Extract:
1. Robot entities (from URDF, config, or class names)
2. Algorithms (classes/functions that implement methods)
3. Skills (procedures in example scripts)
4. API surface (public methods, parameters, return types)
5. Dependencies on other libraries/frameworks
6. Physical constraints encoded in the code (limits, bounds, checks)
```

**Step D — Create Pages with Code Relationships**

Same as paper flow, but `sources` type is `"code"` with confidence 0.6.

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
6. **NEVER create empty pages** — A page with < 200 words of actual extracted content is a stub, not knowledge.
7. **ALWAYS read before extracting** — If the agent has not read the paper text or code, it cannot extract entities. Parsing a README link list does NOT count as reading.
8. **LLM extraction is not optional** — The difference between "structure conversion" and "knowledge alchemy" is the LLM parsing step. Skip it = fail.

## Quick Start Template

```bash
# 1. Fetch raw sources (MUST download, not just parse links)
python rosclaw_fetch.py --input my_awesome.md --output-dir data/raw
# Verify: ls data/raw/papers/ && ls data/raw/code/

# 2. Extract knowledge from EACH source (MUST use LLM)
# For each paper:
python -c "
import fitz, json
doc = fitz.open('data/raw/papers/2301.12345.pdf')
text = '\n'.join(p.get_text() for p in doc)
# Now run LLM prompt on 'text' to extract entities
print('Extracted', len(text), 'chars')
"

# 3. Create wiki pages with extracted content (MUST be >200 words each)
# Use wiki_engine.create_page() or MCP wiki_create_page()

# 4. Add wikilinks between pages (MUST link to >=2 related pages)
# Edit page bodies to include [[Related Page]]

# 5. Update index and lint
python -c "from wiki_engine import update_index; update_index('wiki')"
python -c "from mcp_wiki_server import wiki_auto_lint; wiki_auto_lint()"

# 6. Verify in Obsidian
# Graph View should show interconnected nodes, not isolated stubs
open wiki/
```
