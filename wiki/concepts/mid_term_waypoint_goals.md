---
id: mid_term_waypoint_goals
title: mid-term waypoint goals
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:24:07'
last_reinforced: '2026-04-30T00:24:07'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# Mid-Term Waypoint Goals

**Mid-term waypoint goals** are intermediate spatial targets predicted by a [[VLM global planner]] ⚠️ ⚠️ to guide navigation without requiring full path precomputation. Unlike long-term goals (final destinations) or short-term waypoints (immediate collision avoidance), mid-term waypoints represent a horizon of several meters or a few seconds of travel, providing a coarse trajectory that can be refined by lower-level controllers.

## Definition

In the context of vision-language navigation (VLN), a global planner—typically a large vision-language model (VLM)—outputs a sequence of mid-term waypoint goals from the current observation. Each waypoint is an (x, y) or (x, y, θ) pose in the environment that the robot should reach next. The planner receives semantic cues from the environment (e.g., “go to the kitchen”) and predicts a sparse set of intermediate positions that approximate a feasible path. The robot’s local planner then executes reactive control toward each successive waypoint.

## Role in Navigation

- **Efficiency**: By predicting only a handful of mid-term goals instead of a dense path, the system reduces computational overhead and exploits the VLM’s semantic understanding.
- **Robustness**: If the environment changes (e.g., a door closes), the VLM can recompute a new set of waypoints without redrawing an entire path.
- **Decomposition**: Breaks a complex long-horizon task into manageable sub‑goals, each of which can be verified or adapted online.

## Relationship to Other Concepts

- Used by **[[DualVLN]]** as the output of its global planner, linking high-level instructions to local reactive control.
- Depends on a **[[VLM global planner]] ⚠️ ⚠️** for semantic prediction.
- Contrasts with **short-term waypoints** (e.g., from a local costmap) and **long-term goal** (the final destination in a navigation task).
- Can be integrated with **[[ROS2 Navigation Stack]] ⚠️** by publishing waypoints as `geometry_msgs/PoseStamped` messages.

## Parameters

| Parameter | Description |
|-----------|-------------|
| Definition | Intermediate spatial targets predicted by the VLM global planner to guide navigation without requiring full path precomputation |

## Source

This concept is defined in the paper *DualVLN: A Dual‑Stream Vision‑Language Navigation Framework* (arXiv:2512.08186), which introduces mid-term waypoint goals as a core component of its hierarchical navigation architecture.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `mid-term waypoint goals` --[[related_to]] ⚠️--> `DualVLN` _(wikilink)_
