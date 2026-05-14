---
id: cross_floor_topology_modeling
title: Cross-floor Topology Modeling
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:04:27'
last_reinforced: '2026-04-30T00:04:27'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

# Cross-floor Topology Modeling

**Cross-floor Topology Modeling** is a Multi-Floor Abstraction component that represents the connectivity between different floor levels of a building, primarily through staircases. It enables a robot to understand which areas of each floor are reachable from other floors and to plan traversal routes that cross floor boundaries.

## Functionality

- Models the topological graph of inter-floor connections (e.g., stairwell locations, elevator banks).
- Assigns each floor a node or subgraph within the building's overall connectivity map.
- Allows a path planning system to compute routes that transition between floors, integrating with Stair Climbing ⚠️ or other vertical mobility capabilities.

## Relationships

- **Part of**: Multi-Floor Abstraction – it is the layer that explicitly links floor-level maps.
- **Depends on**: Floor-Level Mapping ⚠️ – the topology model is built per floor before cross-floor edges are defined.
- **Used by**: Cross-Floor Path Planning ⚠️ – any planner that must decide when and where to go up or down stairs uses this model.

## Typical Output

A graph where nodes represent locations (e.g., stairwell entrances on each floor) and edges represent traversability (e.g., staircase segments). This graph can be overlaid on 2D grid maps, semantic floor plans, or SLAM-derived topological graphs.

## Practical Considerations

- Stairway geometry (rise, run, landing dimensions) must be known to validate robot feasibility.
- The model should account for one-way connections (e.g., elevators with access restrictions) and dynamic constraints (e.g., crowd density).
- When used in Sim-to-Real ⚠️ pipelines, the model’s stair parameters can be randomized to increase robustness.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Cross-floor Topology Modeling` --related_to ⚠️--> `Multi-Floor Abstraction` _(wikilink)_
