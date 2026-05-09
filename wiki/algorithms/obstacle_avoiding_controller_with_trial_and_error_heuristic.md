---
id: obstacle_avoiding_controller_with_trial_and_error_heuristic
title: Obstacle-avoiding Controller with Trial-and-Error Heuristic
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:04:07'
last_reinforced: '2026-04-29T21:04:07'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

## Overview

The **Obstacle-avoiding Controller with Trial-and-Error Heuristic** is a low-level control module designed to prevent navigation agents from becoming stuck on obstacles during continuous environment traversal. It forms an integral part of the [[ETPNav]] system, bridging high-level plans with reactive obstacle handling through a simple, repeated-attempt strategy.

## Parameters & Heuristic

- **Type**: low-level control module  
- **Heuristic**: trial‑and‑error — if an action is blocked, the controller systematically tries alternative actions until a traversable path is found or the state is exhausted.  
- **Purpose**: prevent the agent from getting permanently stuck on obstacles (e.g., walls, furniture, dynamic objects) during execution of a long‑horizon plan.

## Capabilities

- Executes high‑level plans issued by [[High-level Planning]] ⚠️ ⚠️ ⚠️ in continuous, unstructured environments.  
- Adapts to obstacles in real‑time via repeated attempts, without requiring explicit obstacle geometry or detailed maps.  
- Operates as a fallback when the planned path becomes infeasible, enabling robust recovery.

## Behavior

When the agent encounters an obstacle, it tries alternative actions in a trial‑and‑error manner until it finds a traversable path. The controller probes nearby directions or velocities, evaluates collision, and selects the first collision‑free option. This iterative search continues until either a clear path emerges or the high‑level planner is called upon to replan.

## Relationships

- **Part of** [[ETPNav]] — the controller is one of the core modules within the ETPNav architecture.  
- **Depends on** [[High-level Planning]] ⚠️ ⚠️ ⚠️ — the controller relies on a high‑level plan (e.g., a sequence of sub‑goals) to guide its local search.  

> *See also:* [[ETPNav]] for the full system overview, and [[High-level Planning]] ⚠️ ⚠️ ⚠️ for the upstream component that directs this controller.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Obstacle-avoiding Controller with Trial-and-Error Heuristic` --[[extends]] ⚠️--> `ETPNav`
