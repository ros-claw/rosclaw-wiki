---
id: topological_mapping
title: Topological mapping
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:19:28'
last_reinforced: '2026-04-30T01:19:28'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# Topological Mapping

## Overview

**Topological mapping** is an online mapping algorithm that constructs a topological representation of an environment without requiring prior experience or pre-built maps. It self-organizes predicted waypoints along a traversed path, enabling a robot to build a compact, graph-like model of traversable space during exploration. The method is designed for embodied navigation tasks where annotation and prior knowledge are unavailable.

This algorithm is a core component of the [[ETPNav]] framework.

## Capabilities

- **Self-organizing predicted waypoints**: The algorithm generates and maintains a set of waypoints that dynamically adjust along the robot's traversal path, forming a connected topological graph.
- **No prior environmental experience required**: It operates solely from online observations, making it suitable for zero-shot navigation in novel environments.

## Relationships

- **part_of**: [[ETPNav]] — Topological mapping serves as a key module within ETPNav, providing a spatial representation that supports downstream planning and navigation behaviors.

## Technical Details

The mapping process is fully online: as the agent moves, it predicts a sparse set of waypoints from its current observation (e.g., using a learned model) and integrates them into a global topological graph. The graph is structured as a set of nodes (waypoints) connected by edges representing traversability. This approach avoids the need for dense metric maps or pre-existing floorplans.

Because the map is constructed incrementally, it naturally adapts to the path taken and can be reused across repeated navigation attempts. The self-organizing mechanism reduces redundancy and ensures coverage of key decision points.

## See Also

- [[Topological Map]] ⚠️ (concept)
- [[Online Mapping]] ⚠️
- [[Waypoint Generation]] ⚠️
- [[Navigation Without Prior Map]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Topological mapping` --[[extends]] ⚠️--> `ETPNav`
