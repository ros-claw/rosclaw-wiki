---
id: stair_aware_obstacle_mapping
title: Stair-aware Obstacle Mapping
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:04:01'
last_reinforced: '2026-04-30T00:04:01'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

## Stair-aware Obstacle Mapping

**Stair-aware Obstacle Mapping** is a concept within [[Multi-Floor Abstraction]] that enables mobile robots to treat staircases not as impassable obstacles but as traversable transitions between floor levels. Unlike conventional obstacle maps that often ignore or block stair geometry, this approach explicitly detects stair geometry and integrates it into the floor map, allowing the robot to reason about multi-floor navigation.

### Capabilities

- **Detects stairs as traversable transitions** — Stair-aware mapping identifies staircases as structured features that connect floor levels, rather than treating them as static obstacles.
- **Incorporates stair geometry into floor maps** — The exact dimensions, slope, and location of stairs are added to the map, enabling path planning that accounts for stair traversal constraints.

### Relationships

- **part_of** [[Multi-Floor Abstraction]] — Stair-aware mapping is a sub-component of the larger framework for representing and navigating multiple floors.
- **depends_on** [[Semantic Mapping]] ⚠️ — Stair recognition relies on semantic labeling of the environment.
- **implements** [[Traversable Transition Detection]] ⚠️ — It is a concrete implementation of detecting transitions between floors.

### Usage Notes

When a robot uses stair-aware obstacle mapping, it can generate paths that include stair climbing, provided the robot is physically capable. The map representation must store stair geometry (riser height, tread depth, width) to ensure feasibility and safety.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Stair-aware Obstacle Mapping` --[[related_to]] ⚠️--> `Multi-Floor Abstraction` _(wikilink)_
