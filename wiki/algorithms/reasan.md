---
id: reasan
title: REASAN
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:29:04'
last_reinforced: '2026-04-29T21:29:04'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

# REASAN

**REASAN** (Reactive Safe Navigation) is a modularized end-to-end framework for legged robot navigation in dynamic environments. It combines three [[Reinforcement Learning|RL policies]] and a [[Transformers|transformer-based estimator]], all trained entirely in simulation, to achieve fully onboard real-time reactive navigation with a single [[LiDAR]] sensor.

## Capabilities

- Fully onboard real-time reactive navigation in complex dynamic environments
- Works with a single [[LiDAR sensor]]
- Supports both single-robot and multi-robot settings
- Modularized end-to-end framework consisting of four simulation-trained modules

## Modules

REASAN decomposes the navigation task into four specialized modules, each trained in simulation using [[reinforcement learning]]:

1. **Locomotion RL Policy** – controls the robot's base motion
2. **Safety Shielding RL Policy** – ensures collision avoidance and safe operation
3. **Navigation RL Policy** – guides the robot toward a goal
4. **Transformer-based Exteroceptive Estimator** – processes LiDAR scans to perceive dynamic obstacles

All modules are trained via [[curriculum learning]] ⚠️ ⚠️ and [[reward shaping]] to enable robust sim-to-real transfer.

## Relationships

- **Uses**: [[RL policy for locomotion]], [[RL policy for safety shielding]], [[RL policy for navigation]] ⚠️, [[transformer-based exteroceptive estimator]], [[LiDAR sensor]]
- **Depends on**: [[reinforcement learning]], [[simulation training]] ⚠️, [[curriculum learning]] ⚠️ ⚠️, [[reward shaping]]

## See also

- [[Unitree G1]] (often used as a test platform for REASAN)
- [[Sim-to-Real Transfer]]
- [[Reactive Navigation]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `REASAN` --[[implements]] ⚠️--> `Unitree G1`
