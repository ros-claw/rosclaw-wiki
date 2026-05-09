---
id: reasan_reactive_safe_navigation
title: REASAN (Reactive Safe Navigation)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:22:19'
last_reinforced: '2026-04-30T03:22:19'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

# REASAN (Reactive Safe Navigation)

**REASAN** (Reactive Safe Navigation) is a modularized end-to-end framework for legged reactive navigation using a single LiDAR sensor. It consists of four simulation-trained modules: three [[Reinforcement Learning]] (RL) policies (locomotion, safety shielding, navigation) and a transformer-based exteroceptive estimator.

## Overview

REASAN is designed to enable fully onboard real-time reactive navigation in complex dynamic environments, supporting both single- and multi-robot settings. The system uses only a single [[LiDAR]] sensor as input, trained entirely in simulation, and deployed without fine-tuning. The modular architecture decouples locomotion, safety, and navigation, while the transformer-based estimator provides robust environmental perception.

## Modules

- **Locomotion Policy** – Controls base motion (e.g., velocity, posture) for the legged robot.
- **Safety Shielding Policy** – Supervises commands to prevent collisions or unsafe actions.
- **Navigation Policy** – Plans high-level goals based on estimated traversability and obstacle avoidance.
- **Exteroceptive Estimator** – A [[Transformer]] ⚠️ ⚠️ architecture that processes LiDAR scans into a representation of the environment, feeding the navigation policy.

## Capabilities

- Fully onboard real-time reactive navigation
- Navigation in complex dynamic environments
- Single- and multi-robot settings

## Training

The three RL policies are trained in simulation using [[curriculum design]] and [[reward shaping]]. The modularized approach allows each policy to be optimized for its specific role. The system is simulation-trained and deployed directly to real hardware without domain randomization or fine-tuning.

## Code Release

Training and deployment code is publicly available: [REASAN on GitHub](https://github.com/ASIG-X/REASAN).

## Relationships

- **Uses**: [[LiDAR]], [[RL policies]] ⚠️, [[Transformer]] ⚠️ ⚠️
- **Depends on**: [[curriculum design]], [[reward shaping]]
- **Implements**: [[modularized end-to-end framework]] ⚠️, [[reactive navigation]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `REASAN (Reactive Safe Navigation)` --[[implements]] ⚠️--> `LiDAR`
