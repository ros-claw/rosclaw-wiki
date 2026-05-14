---
id: embodied_spatial_reasoning
title: Embodied Spatial Reasoning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:58:52'
last_reinforced: '2026-04-30T02:58:52'
supersedes: []
sources:
- papers/2602.18424.pdf
source_type: arxiv_paper
---

# Embodied Spatial Reasoning

**Embodied Spatial Reasoning** is the ability of an AI system to reason about spatial relationships and physical constraints relevant to an embodied agent. This includes understanding whether an object or path is navigable given the agent’s size, shape, and mobility, as well as predicting the consequences of agent–environment interactions.

## Capabilities

- **Spatial dimension and obstacle constraint reasoning** — evaluating if a passage or manipulation is feasible.
- **Understanding agent–environment interactions** — modeling how the agent’s body and actions affect and are affected by the surrounding space.

## Context

Embodied Spatial Reasoning is a component of Capability-Conditioned Navigation (CapNav), where navigation decisions depend on the agent’s own physical capabilities rather than assuming a generic point robot. It complements other perceptual and planning skills such as Occupancy Mapping (https://en.wikipedia.org/wiki/Occupancy_grid_mapping) ⚠️ and Motion Planning ⚠️.

## Relation to Other Concepts

- **depends_on**: Embodied AI, Spatial Understanding ⚠️
- **part_of**: Capability-Conditioned Navigation (CapNav)
- **implements**: Agent-Centric Navigation ⚠️

## Sources

- *Embodied Spatial Reasoning for Capability-Conditioned Navigation* (arXiv:2602.18424)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Embodied Spatial Reasoning` --related_to ⚠️--> `Embodied AI`
