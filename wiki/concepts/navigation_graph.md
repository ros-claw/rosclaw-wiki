---
id: navigation_graph
title: Navigation Graph
type: concept
tags: []
confidence: 0.6
created_at: '2026-04-30T04:53:53'
last_reinforced: '2026-04-30T04:53:53'
supersedes: []
sources:
- articles/wildos.md
source_type: blog_post
---

## Navigation Graph

A **Navigation Graph** is a sparse topological representation of an environment used for robot navigation. It encodes spatial structure as a graph where nodes represent distinct locations (e.g., geometric frontier nodes, free nodes) and edges encode connectivity between them. Unlike dense occupancy maps or metric grids, a navigation graph prioritizes tractable planning and persistent spatial memory, making it well-suited for long-horizon exploration in unstructured or partially known environments.

### Key Parameters

- **Type:** Sparse navigation graph
- **Nodes:** Geometric frontier nodes (regions at the boundary between known and unknown space), free nodes (already explored or traversable locations)
- **Edges:** Connectivity between nodes, indicating feasible paths

### Capabilities

- Maintains **persistent spatial memory** across exploration sessions, enabling the robot to remember where it has been and which areas remain unexplored
- Identifies **geometric frontier nodes** that represent safe, informative exploration targets
- Enables **replanning from dead-ends** by allowing the robot to backtrack along stored graph edges and choose alternative frontier nodes

### Role in WildOS

WildOS builds a sparse navigation graph from geometric sensing to maintain persistent spatial memory and identify geometric frontier nodes. These geometric frontier nodes are then projected into the camera image and scored using visual-semantic cues from ExploRFM, producing a semantically scored graph. This integrated representation allows WildOS to choose exploration goals that are both geometrically safe and semantically meaningful (e.g., “explore toward the dark opening”, “avoid the crumbling ledge”).

### Relationships

- **Used by:** WildOS (depends on the navigation graph for spatial reasoning and frontier selection)
- **Related to:** Geometric Frontiers ⚠️ (the specific frontier type used as nodes), Visual Frontiers ⚠️ (an alternative frontier definition based on visual/semantic information)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Navigation Graph` --related_to ⚠️ ⚠️--> `WildOS` _(wikilink)_
- `Navigation Graph` --related_to ⚠️ ⚠️--> `ExploRFM` _(wikilink)_
