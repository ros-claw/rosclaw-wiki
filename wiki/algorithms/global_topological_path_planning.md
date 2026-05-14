---
id: global_topological_path_planning
title: Global Topological Path Planning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:36:46'
last_reinforced: '2026-04-29T21:36:46'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

## Global Topological Path Planning

**Global Topological Path Planning** is an algorithm class for long-horizon robot navigation that operates on a topological abstraction of the environment rather than a continuous metric map. It represents the goal as object-level sub-goals, enabling planning over extended time horizons without requiring a global metric representation.

### Overview

Traditional path planning relies on metric maps (e.g., occupancy grids, point clouds) which become computationally expensive and brittle over large distances or unstructured environments. Global topological path planning bypasses this by building a graph of distinct places or regions, connected by navigable edges. The planner reasons over this graph, selecting sequences of sub-goals that lead from the current region to the target region.

### Parameters

| Parameter | Value |
|-----------|-------|
| Type | Topological |
| Goal representation | Object-level sub-goals |

Object-level sub-goals refer to semantically meaningful landmarks (e.g., "doorway", "kitchen counter", "charging station") rather than coordinates. This aligns the planner with human-like cognitive spatial reasoning.

### Capabilities

- **Long-horizon planning without global metric maps** – Avoids the complexity and drift of metric SLAM over long trajectories.
- **Integration with local metric control** – The topological plan provides a sequence of waypoint sub-goals; each sub-goal is executed by a local metric planner (e.g., DWA, MPC) that navigates precisely within the current region.

### Relationships

- **Part of** TANGO – TANGO (Topological Action Graph for Navigation in Global Operations) is an architecture that uses global topological path planning as its core reasoning layer. The planner selects sub-goal sequences from TANGO's object-level graph.
- **Depends on** Foundational Models ⚠️ ⚠️ – These models provide semantic understanding of objects and scenes to construct and update the topological graph (e.g., object detection, open-vocabulary segmentation, and spatial reasoning from vision-language models).

### Section in TANGO

Within TANGO, global topological path planning sits above the metric control stack. It receives a go-to-object command, retrieves the relevant object-level sub-goals from the topological graph, and outputs an ordered list of intermediate targets for the local planner.

### Related Pages

- TANGO – The architecture that employs this algorithm.
- Foundational Models ⚠️ ⚠️ – Enablers of semantic graph construction.
- Topological Navigation ⚠️ – Broader concept covering graph-based navigation strategies.
- Object-Level Representations ⚠️ – How objects are treated as nodes in the topological graph.
- Long-Horizon Planning – Problem setting that this algorithm addresses.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Global Topological Path Planning` --extends ⚠️--> `TANGO`
