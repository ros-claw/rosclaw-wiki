---
id: mapless_path_planning
title: Mapless Path Planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:42:24'
last_reinforced: '2026-04-30T04:42:24'
supersedes: []
sources:
- papers/2511.17792.pdf
source_type: arxiv_paper
---

# Mapless Path Planning

## Definition
**Mapless Path Planning** is a navigation paradigm that plans a path to a semantic goal without relying on a pre-built metric map. Instead, it leverages predictions from a video world model to guide motion. The approach allows the robot to navigate in unknown or changing environments by understanding high-level task instructions rather than precise spatial coordinates.

## Capabilities
- Navigate toward a semantic target (e.g., “go to the kitchen table”) without an explicit metric map.
- Uses a video world model to simulate possible future trajectories and select actions that reach the goal.
- Operates in zero-shot settings where no prior map of the environment is available.

## Evaluation
This concept is evaluated by Target-Bench, a benchmarking framework designed to test semantic goal‑conditioned navigation without maps.

## Related Concepts
- Semantic Navigation ⚠️ — navigation governed by language or categorical goals.
- Video World Model ⚠️ — the predictive model that substitutes for a classical metric map.
- Path Planning ⚠️ — the broader field of generating motion trajectories.
- Implicit Map Representation ⚠️ — alternative to explicit maps, often used in mapless systems.

## References
- arxiv paper 2511.17792 — describes the method and its evaluation on Target-Bench.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Mapless Path Planning` --applies_to ⚠️--> `Target-Bench`
