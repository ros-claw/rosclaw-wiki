---
id: tango
title: TANGO
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:35:35'
last_reinforced: '2026-04-29T21:35:35'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# TANGO

**TANGO** is a novel RGB-only, object-level topometric navigation pipeline that integrates global topological path planning with local metric trajectory control. It operates without globally-consistent 3D maps or learned controllers, using foundational models for open-set generalization.

## Overview

TANGO achieves zero-shot long-horizon robot navigation without requiring pre-built 3D maps or pre-trained controllers. Its open-set applicability is enabled by foundational models, and it performs obstacle avoidance via local metric trajectory control. An auto-switching mechanism allows the system to fall back to a baseline controller when necessary, ensuring robustness.

## Components

The TANGO system is composed of four key modules:

- **Global Topological Path Planning** – responsible for long-horizon navigation by reasoning over object-level semantic landmarks.
- **Local Metric Trajectory Control** – handles real-time obstacle avoidance and fine-grained motion within local spaces.
- **Monocular Depth and Traversability Estimation** – uses RGB-only input to estimate depth and assess terrain traversability.
- **Auto-Switching Mechanism** – automatically falls back to a baseline (e.g., reactive) controller when the learned planner is unreliable or safety-critical.

## Parameters

| Parameter | Value |
|-----------|-------|
| Input modality | RGB-only |
| Output | Object-level topometric navigation |
| Supporting estimation | Monocular depth and traversability |

## Dependencies & Relationships

- Uses: Global Topological Path Planning, Local Metric Trajectory Control, Monocular Depth and Traversability Estimation, Auto-Switching Mechanism
- Depends on: Foundational Models ⚠️, Monocular Depth Estimation ⚠️
- Implements: Object-Level Topometric Navigation

## Performance

TANGO outperforms existing state-of-the-art methods in both simulated and real-world tests, demonstrating robustness and deployability. It excels in open-world settings where prior 3D maps or task-specific controllers are unavailable.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `TANGO` --extends ⚠️ ⚠️ ⚠️ ⚠️--> `Global Topological Path Planning`
- `TANGO` --extends ⚠️ ⚠️ ⚠️ ⚠️--> `Local Metric Trajectory Control`
- `TANGO` --extends ⚠️ ⚠️ ⚠️ ⚠️--> `Monocular Depth and Traversability Estimation`
- `TANGO` --extends ⚠️ ⚠️ ⚠️ ⚠️--> `Auto-Switching Mechanism`
