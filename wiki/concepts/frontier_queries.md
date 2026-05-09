---
id: frontier_queries
title: Frontier queries
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:58:59'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

---

# Frontier Queries

**Frontier queries** represent unexplored locations in an environment, specifically used within the [[Unified objective for grounding and exploring]] to select where the agent should navigate next. These queries encode spatial uncertainty and serve as targets for simultaneous grounding (associating language with physical locations) and exploration.

In practice, a frontier query may be expressed as a set of candidate points or regions that are both promising for reducing environmental uncertainty and relevant to the agent’s current language grounding task. By integrating frontier queries into a single optimization framework, the unified objective balances exploration (visiting unknown areas) and grounding (confirming or updating semantic associations).

### Type and Purpose

Frontier queries are a **representation** type whose primary **purpose** is to represent unexplored locations in the environment. This representation enables the agent to reason about where to go next in a structured, optimizable form.

### Capabilities

- **Enable joint optimization of object grounding and frontier selection** – By encoding spatial uncertainty and language‑relevant regions, frontier queries allow the unified objective to simultaneously decide where to move and which semantic associations to verify, leading to more efficient exploration and grounding.

### Relationships

- [[Unified objective for grounding and exploring]] → uses → **Frontier queries**
- **Frontier queries** → used_by → [[MTU3D]] (the 3D multi‑target grounding and exploration framework)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Frontier queries` --[[related_to]] ⚠️--> `Unified objective for grounding and exploring` _(wikilink)_