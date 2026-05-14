---
id: dual_relation_reasoning
title: Dual-relation reasoning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:03:42'
last_reinforced: '2026-04-30T00:03:42'
supersedes: []
sources:
- papers/2512.02400.pdf
source_type: arxiv_paper
---

# Dual-Relation Reasoning

**Dual-relation reasoning** is a conceptual framework used in Nav-R^2 that explicitly models two critical types of relationships to improve navigation and decision-making in embodied agents. It separates reasoning into **target–environment modeling** and **environment–action planning**, allowing the agent to understand how goals relate to the environment and how the environment informs action sequences.

## Capabilities

- **Target–environment modeling**: Learns the relationships between navigation targets (e.g., destination objects or locations) and the surrounding environmental context (e.g., obstacles, landmarks, traversability).
- **Environment–action planning**: Models the mapping from environmental state to appropriate motor actions or navigation policies, enabling efficient path execution.

## Relationship

- **part_of**: Nav-R^2 — Dual-relation reasoning is a core component of the Nav-R^2 architecture.

## Source

- arXiv paper: [2512.02400](https://arxiv.org/abs/2512.02400)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Dual-relation reasoning` --related_to ⚠️--> `Nav-R^2` _(wikilink)_
