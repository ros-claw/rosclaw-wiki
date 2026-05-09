---
id: frontier_ranking
title: Frontier Ranking
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:05:00'
last_reinforced: '2026-04-30T00:05:00'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

# Frontier Ranking

**Frontier Ranking** is a concept within [[Coarse-to-Fine Reasoning]] that selects promising exploration frontiers during a coarse exploration step. It acts as a filtering mechanism to prioritize regions of interest before finer-grained analysis or action selection.

## Capabilities

- Selects promising exploration frontiers
- Coarse exploration step

## Relationships

- **part of** [[Coarse-to-Fine Reasoning]]
- **uses** [[Frontier Detection]] ⚠️ to identify candidate regions
- **depends_on** [[Exploration Policy]] to define criteria for "promising"
- **implements** a filtering function that reduces the state space for subsequent fine-grained reasoning

## Source

- arxiv paper 2505.23019 (Coarse-to-Fine Reasoning for Embodied Exploration)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Frontier Ranking` --[[related_to]] ⚠️--> `Coarse-to-Fine Reasoning` _(wikilink)_
