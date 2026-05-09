---
id: hierarchical_planning
title: Hierarchical Planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:21:45'
last_reinforced: '2026-04-30T00:21:45'
supersedes: []
sources:
- papers/2512.01550.pdf
source_type: arxiv_paper
---

# Hierarchical Planning

**Hierarchical Planning** is a conceptual framework in which a high-level task is recursively decomposed into a sequence of finer-grained sub-tasks. This multi-level abstraction allows an agent to reason and execute at varying granularities, improving computational efficiency, robustness, and interpretability.

## Definition

Hierarchical planning breaks down a high-level task into a sequence of lower-level sub-tasks, enabling an agent to plan at multiple levels of abstraction for efficiency and robustness.

## Capabilities

- Decompose complex long-horizon tasks into manageable sub-goals
- Enable structured reasoning and execution
- Reduce the search space for decision-making

## Relationships

This concept is **implemented by** [[NavForesee]], which uses hierarchical planning to navigate dynamic environments.

## Related Concepts

- [[Task Planning]] ⚠️ – broader discipline of sequencing actions.
- [[Hierarchical Task Networks]] ⚠️ – a classical AI planning formalism closely related to hierarchical planning.
- [[Sim-to-Real Transfer]] – often benefits from hierarchical decomposition to bridge simulation and reality.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Hierarchical Planning` --[[related_to]] ⚠️--> `NavForesee` _(wikilink)_
