---
id: mobility_aware_local_navigation_planning
title: Mobility-Aware Local Navigation Planning
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-29T21:44:32'
last_reinforced: '2026-04-29T21:44:32'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

# Mobility-Aware Local Navigation Planning

**Mobility-Aware Local Navigation Planning** is an embodied AI skill that generates feasible local trajectories by explicitly considering the robot’s locomotion capabilities—such as ground clearance, wheel slip, leg articulation, and terrain compliance. It bridges high-level path planning and low-level control, enabling high-speed, agile movement through cluttered or unstructured environments.

## Overview

Traditional local planners treat the robot as a rigid body with simple kinematic constraints. In contrast, mobility-aware planning leverages real-time estimates of the robot’s mobility envelope (e.g., reachable footholds, torque limits, stability margins) to produce trajectories that are dynamically feasible. This approach is critical for Wheeled-Legged Robots ⚠️ such as the Unitree G1 or ANYmal, where hybrid locomotion modes require adaptive terrain responses.

## Capabilities

- Plan smooth paths in cluttered environments  
- Adapt to terrain and obstacles in real-time  
- Integrate with a low-level locomotion controller ⚠️ ⚠️ to execute motion commands  

## Parameters

| Parameter       | Value                                          |
|-----------------|------------------------------------------------|
| Planning type   | Local navigation                               |
| Awareness       | Mobility-aware (considers locomotion capabilities) |

## Role

Generates feasible local trajectories that respect the robot’s locomotion constraints, allowing high-speed navigation through complex environments. By embedding mobility forecasts into the cost function and constraint set, the planner can safely negotiate dynamic obstacles, slopes, stairs, and deformable terrain without relying on conservative slowdowns.

## Relationships

- **part_of** → Autonomous Navigation for Wheeled-Legged Robots  
- **uses** → Hierarchical Reinforcement Learning (to learn mapping from state/mobility to optimal local paths)  

## Implementation Notes

In practice, the planner often runs as a ROS node subscribing to:

- `/move_base_simple/global_plan` (global path from a top-level planner)  
- `/odometry` and `/joint_states`  
- `/elevation_map` or `/terrain_costmap`  

It publishes a locally smoothed path (e.g., on `/local_plan`) that the low-level locomotion controller ⚠️ ⚠️ tracks via inverse kinematics or model-predictive control (MPC ⚠️). The mobility model can be pre-computed from the robot’s digital twin or learned online through Reinforcement Learning.

## Related Skills

- Global Path Planning ⚠️ (provides the high‑level route to be refined)  
- Terrain Traversability Estimation ⚠️ (feeds mobility constraints)  
- Locomotion Control ⚠️ (executes the planned trajectories)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Mobility-Aware Local Navigation Planning` --[[operates_on]] ⚠️ ⚠️--> `Unitree G1`
- `Mobility-Aware Local Navigation Planning` --[[operates_on]] ⚠️ ⚠️--> `ANYmal`
- `Mobility-Aware Local Navigation Planning` --uses ⚠️--> `Hierarchical Reinforcement Learning`
**Pending review:**
- `Mobility-Aware Local Navigation Planning` --related_to ⚠️--> `Autonomous Navigation for Wheeled-Legged Robots` _(wikilink)_
