---
id: reactive_navigation
title: Reactive Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:30:55'
last_reinforced: '2026-04-30T03:30:55'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

## Reactive Navigation

Reactive navigation refers to the ability of a robot to navigate by reacting to sensor inputs in real-time, without relying on a [[global plan]] ⚠️. It is a core paradigm in [[embodied AI]] and [[autonomous robotics]] ⚠️ where the robot must operate in dynamic or unknown environments. This approach contrasts with [[deliberative navigation]] ⚠️ that requires a precomputed path.

### Definition

Reactive navigation represents the capability of an autonomous system to generate movement commands directly from sensor observations, enabling rapid adaptation to changes in the environment. It is characterized by a tight coupling between sensing and action, often implemented as a set of [[behavioral rules]] ⚠️ or [[neural policies]] ⚠️.

### Capabilities

- **Real-time obstacle avoidance**: Obstacles detected by sensors (e.g., [[LiDAR]], [[depth cameras]] ⚠️) cause immediate course corrections without waiting for a replanning cycle.
- **No pre-planned path required**: The robot does not maintain a map or global trajectory; instead, it continuously selects the next action based on current local observations. This is especially useful in [[unstructured environments]] ⚠️ or during [[sim-to-real]] ⚠️ deployment.

### Relationships

- **Part of**: Reactive navigation is a foundational component of the [[REASAN]] system (Reactive Environment-Aware Semantic Autonomous Navigation). Within REASAN, reactive navigation works alongside [[semantic perception]] ⚠️ and [[local planning modules]] ⚠️ to achieve robust autonomous behavior.

### Usage Context

Reactive navigation typically operates at a high update frequency (>10 Hz) and is often implemented using [[reactive control laws]] ⚠️, [[potential fields]] ⚠️, or [[learned policies]] ⚠️ from [[reinforcement learning]]. It is commonly combined with a [[global planner]] ⚠️ in hybrid architectures, but the reactive layer handles immediate hazard avoidance.

---

**Sources**:  
- Paper: *REASAN: Reactive Environment-Aware Semantic Autonomous Navigation* (arXiv:2512.09537)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Reactive Navigation` --[[related_to]] ⚠️ ⚠️--> `embodied AI`
- `Reactive Navigation` --[[applies_to]] ⚠️--> `LiDAR`
**Pending review:**
- `Reactive Navigation` --[[related_to]] ⚠️ ⚠️--> `REASAN` _(wikilink)_
