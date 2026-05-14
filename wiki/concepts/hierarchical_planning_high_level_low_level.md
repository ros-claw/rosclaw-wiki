---
id: hierarchical_planning_high_level_low_level
title: Hierarchical Planning (High-level + Low-level)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:04:42'
last_reinforced: '2026-04-29T21:04:42'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

## Hierarchical Planning (High-level + Low-level)

**Hierarchical Planning** is an architectural paradigm that decomposes autonomous navigation into two distinct layers: *high-level planning* for abstract waypoint selection and *long-horizon reasoning*, and *low-level control* for local obstacle-avoiding motion. This separation of concerns allows the agent to manage both global task structure and local dynamics without coupling them tightly.

### Overview

In standard navigation stacks, planning and control are often integrated, leading to computational bottlenecks or fragility in cluttered environments. Hierarchical Planning mitigates this by introducing a **planner-controller hierarchy**:

- **High-level planner** – reasons about topology, sequential goals, or semantic landmarks. It outputs coarse waypoints or subgoals that are invariant to local geometry.
- **Low-level controller** – executes smooth, collision-free motion between those waypoints. It reacts to local sensor data (e.g., LiDAR, depth images) and handles dynamic obstacles.

This architecture is especially effective in **long-horizon tasks** where the agent must traverse multiple rooms, corridors, or outdoor areas.

### Capabilities

- **Enables long-horizon tasks** – the high-level planner can maintain a global map or topological graph while the low-level controller ensures safe motion.
- **Improves robustness in complex environments** – failures at one layer (e.g., a blocked path) can be handled by re‑planning at the high level without recomputing low-level trajectories from scratch.

### Benefits

Separating planning and control allows the agent to reason at a higher level of abstraction while the low-level controller handles local dynamics and obstacles. This reduces computational complexity, improves generalization across environments, and makes the system more interpretable (each layer’s outputs are distinct and debuggable).

### Relationships

- **used_by** – ETPNav implements hierarchical planning to achieve robust vision-language navigation across unseen environments.
- **part_of** – The paradigm is a key component of Vision-Language Navigation systems that require both semantic understanding and real‑world action.
- **depends_on** – High-level planning often relies on Semantic Mapping ⚠️ or Topological Graphs ⚠️, while low-level control integrates Reactive Control ⚠️ or Model Predictive Control ⚠️.

### See Also

- ETPNav
- Vision-Language Navigation
- Hierarchical Reinforcement Learning
- Sim-to-Real Transfer (for training the low-level controller)

*Source: arXiv:2304.03047*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Hierarchical Planning (High-level + Low-level)` --related_to ⚠️--> `ETPNav` _(wikilink)_
