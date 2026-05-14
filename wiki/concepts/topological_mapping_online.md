---
id: topological_mapping_online
title: Topological Mapping (Online)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:03:13'
last_reinforced: '2026-04-29T21:03:13'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# Topological Mapping (Online)

Topological Mapping (Online) is an online mapping method in which the agent self-organizes predicted waypoints along a traversed path to create a topological map **without prior environmental experience**. Unlike traditional SLAM-based approaches that require geometric consistency, this method incrementally builds a sparse graph of nodes (waypoints) and edges (traversable connections) purely from the robot’s own navigation predictions.

## Capabilities

- Enables long-range navigation planning in unknown environments  
- Avoids the need for pre-built maps or prior exploration  
- Supports real-time adaptation as the agent explores  

## Mechanism

The agent incrementally builds a topological map by clustering the waypoints it predicts during navigation. Each predicted waypoint becomes a candidate node; as the robot moves, waypoints that are spatially and temporarily close are merged or linked into edges. The resulting graph represents traversable paths that the agent has actually **experienced**, even if the environment was previously unseen. This self-organizing process allows the map to grow and refine itself without any external supervision or preloaded map data.

## Related Pages

- **Used by**: ETPNav employs this online topological mapping method to plan long-horizon trajectories.
- **Depends on**: Waypoint Prediction ⚠️, which provides the initial point estimates that are clustered into topological nodes.

## Source

- ArXiv paper 2304.03047: *ETPNav: Evolving Topological Planning for Vision-Language Navigation in Continuous Environments*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Topological Mapping (Online)` --related_to ⚠️--> `ETPNav` _(wikilink)_
