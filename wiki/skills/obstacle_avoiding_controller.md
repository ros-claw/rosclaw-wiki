---
id: obstacle_avoiding_controller
title: Obstacle-avoiding controller
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T01:20:26'
last_reinforced: '2026-04-30T01:20:26'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

## Obstacle-avoiding controller

The **obstacle-avoiding controller** is a low-level control skill designed to prevent a navigation agent from getting stuck on obstacles during autonomous navigation. It is a core component of the ETPNav framework and employs a **trial-and-error** heuristic to dynamically adjust the robot's behavior when faced with blockages or collision risks.

### Overview

In complex environments, standard path planners may lead a robot into dead ends or cause repeated collisions. The obstacle-avoiding controller provides a reactive mechanism that detects impending stalls or contacts and attempts alternative maneuvers. Its heuristic, trial-and-error, means it quickly tests small deviations from the planned trajectory until a feasible escape path is found. This makes the controller particularly suited for cluttered and dynamic settings where global replanning would be too slow.

### Parameters

| Parameter  | Value            | Description                                                                 |
|------------|------------------|-----------------------------------------------------------------------------|
| **heuristic** | `trial-and-error` | The decision-making strategy used to explore alternative actions around obstacles. |

### Capabilities

- **Prevents navigation from getting stuck in obstacles** – The controller continuously monitors the robot's progress; if forward motion is blocked or the robot becomes stuck, it triggers the trial-and-error heuristic to generate a recovery behavior.

### Relationships

- **part_of** ETPNav – This controller is one of the low-level skills within the ETPNav system, which combines high-level topological planning with reactive obstacle avoidance.

### Source

The description is derived from:  
`data/raw/papers/2304.03047.pdf` – "ETPNav: Evolving Topological Planning for Robot Navigation in Dynamic Environments" (arxiv).

---

**Cross-references:** [[navigation]] ⚠️, obstacle avoidance ⚠️, low-level control ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Obstacle-avoiding controller` --uses ⚠️--> `ETPNav`
