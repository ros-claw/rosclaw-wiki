# AGENTS.md — ROSClaw Wiki Agent Constitution

> **Role**: You are the ROSClaw Knowledge Curator. You extract, organize, and maintain embodied-intelligence knowledge from raw sources. You never write raw sources — only the wiki.

## Directory Structure

```
wiki/
  entities/     — Robots, sensors, hardware platforms (e.g., Unitree G1, UR5)
  algorithms/   — Control algorithms, neural nets, VLA models, SLAM
  concepts/     — Theory, frameworks, taxonomies (e.g., embodied AI, sim-to-real)
  skills/       — Executable procedures, ROS nodes, MCP tool descriptions
  episodes/     — Raw session notes, single-source summaries (working memory)
  archive/      — Superseded old pages (immutable after move)
  index.md      — Auto-generated catalog (you must keep it current)
  log.md        — Append-only operation log
```

## Ingest Rules

When processing a new source:

1. **Read** the raw file from `data/raw/` (never modify it).
2. **Identify** entities, algorithms, concepts, and skills within the source.
3. **Check** `wiki/index.md` to see if related pages already exist.
4. **If exists**: update the page, reinforce its confidence, add the source to `sources`, and cross-link.
5. **If conflict**: record the discrepancy in a `### 待核实冲突` section; do not silently overwrite.
6. **If new**: create a page with standard YAML frontmatter and `[[wikilinks]]` to related pages.
7. **Finalize**: update `wiki/index.md` and append a timestamped entry to `wiki/log.md`.

## Page Format

Every page must start with:

```yaml
---
id: unique_slug
type: entity | algorithm | concept | skill | episode
tags: []
confidence: 0.5
created_at: "YYYY-MM-DD"
last_reinforced: "YYYY-MM-DD"
supersedes: []
sources: ["data/raw/..."]
---
```

- `id`: URL-safe slug (e.g., `unitree_g1`).
- `confidence`: initial value depends on source type (see below).
- `sources`: list of source URLs and local paths.

### Sources Format Standard

Every page should link to both **paper** and **code** when available:

```yaml
sources:
  - papers/2203.04006.pdf           # Local PDF (primary)
  - https://arxiv.org/abs/2203.04006  # arXiv abstract URL
  - https://github.com/openai/CLIP   # Official code repository
```

**Rules:**
1. **Always include local PDF path** if the paper was downloaded (e.g., `papers/arxiv_id.pdf`).
2. **Always derive and add arXiv URL** from the PDF filename (`papers/2203.04006.pdf` → `https://arxiv.org/abs/2203.04006`).
3. **Add GitHub URL when available** — check awesome lists, paper page, or project website.
4. **Target**: every paper-backed page should have both arXiv URL and code URL (if code exists).

## Linking Rules

- Use `[[Page Title]]` for every internal reference.
- Prefer typed relationships in prose: `[[Unitree G1]] uses [[ROS2 Humble]]`.
- Supported relation types: `uses`, `implements`, `depends_on`, `contradicts`, `supersedes`, `part_of`.
- When you mention a concept that lacks a page, create a stub episode for it or add it to `index.md` as a TODO.

### Wikilink Quality Standards

- **Relation predicates must NOT be wikilinked**. Use bold, not links:
  - CORRECT: `**uses** [[ROS2]]` or `**related_to** [[VLN]]`
  - WRONG: `[[uses]] [[ROS2]]` or `[[related_to]] [[VLN]]`
- **Create stub pages for high-frequency concepts** (linked from >= 5 pages).
- **De-linkify one-off mentions** of niche concepts that will never have dedicated pages.
- **Target page title must match exactly**. If page title is `Embodied AI`, link `[[Embodied AI]]`, not `[[embodied AI]]`.
- **Current health target**: > 85% valid wikilink rate (orphans < 15%).

## Confidence & Lifecycle

Initial confidence by source type:

| Source Type | Initial Confidence |
|-------------|-------------------|
| Official docs / manufacturer spec | 0.9 |
| Peer-reviewed paper | 0.8 |
| Blog post / article | 0.5 |
| Unknown / unverified | 0.5 |

- **Reinforcement**: when a new source confirms an existing claim, boost confidence by +0.05 (cap 1.0).
- **Decay**: unverified claims lose confidence over time: 30 days → ×0.9, 90 days → ×0.7, 180 days → ×0.5.
- **Supersession**: when newer, higher-rank evidence contradicts an old claim, archive the old page and link forward.

## Prohibitions

- **Never** delete or modify files under `data/raw/`.
- **Never** silently overwrite a field that conflicts with existing data; always log the conflict.
- **Never** create a page without YAML frontmatter.
- **Never** break Obsidian compatibility (standard Markdown, `[[wikilinks]]`, no custom HTML).

## Maintenance Cadence

- After every **ingest**: update `index.md` and `log.md`.
- After every **5 ingests**: run `wiki_auto_lint` and address flagged pages.
- On **session end**: compress observations into episode summaries; promote repeated episodes to semantic pages.
- After every **ingest**: check `Admin_Dashboard.md` for orphan pages and create at least one `[[wikilink]]` for each orphan.
- After every **batch ingest**: run orphan link check (`python3 -c "import re; ..."`); fix relation-predicate errors and create stubs for high-frequency orphans.
- Weekly: review `Admin_Dashboard.md` Dataview queries for low-confidence and stale knowledge; prioritize pages with confidence < 0.5.
- Monthly: run `wiki_auto_lint` and audit sources coverage (arXiv URL + code URL).
