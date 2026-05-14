---
id: eb_navigation
title: EB-Navigation
type: entity
tags: []
confidence: 0.6
created_at: '2026-04-29T21:54:58'
last_reinforced: '2026-04-29T21:54:58'
supersedes: []
sources:
- articles/article.md
source_type: blog_post
---

# EB-Navigation

**EB-Navigation** is a component of the EmbodiedBench suite that evaluates an agent’s ability to perform low‑level navigation tasks in simulated environments. It requires the agent to produce low‑level actions (translational and rotational control) to reach a goal, demanding precise perception and spatial reasoning.

## Capabilities

- **Low‑level planning** – The agent must generate sequences of velocity commands to move the robot through the environment.
- **Spatial reasoning** – Understanding the geometry of the surroundings, obstacles, and goal locations.
- **Precise perception** – Reliable sensing (e.g., depth, RGB) is required to localise and avoid collisions.

## Parameters

| Parameter      | Value        |
|----------------|--------------|
| Action level   | low‑level    |
| Description    | Requires planning with low‑level actions (translational/rotational control), demands precise perception and spatial reasoning |

## Relationships

- **part_of** → EmbodiedBench — EB‑Navigation is one of several tasks within the EmbodiedBench benchmark.

## Usage

Agents evaluated on EB‑Navigation typically receive sensor observations (e.g., egocentric camera, odometry) and must output continuous velocity commands (`linear.x`, `angular.z`) to navigate to a specified target. Success is measured by reaching the goal within a time limit while avoiding collisions.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EB-Navigation` --depends_on ⚠️--> `EmbodiedBench`
