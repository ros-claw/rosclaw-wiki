---
id: model_free_reinforcement_learning
title: Model-Free Reinforcement Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:41:26'
last_reinforced: '2026-04-29T21:41:26'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

## Overview

**Model-Free Reinforcement Learning (MFRL)** is a class of reinforcement learning algorithms that learn optimal policies directly from interaction with the environment, without requiring or learning an explicit model of the system dynamics. In robotics, MFRL is particularly effective for complex, high‑dimensional control tasks where accurate dynamics models are difficult to obtain. This page documents the application of MFRL to locomotion controller development for wheeled‑legged robots.

## Parameters

| Parameter          | Value                              |
|--------------------|------------------------------------|
| Learning method    | Model‑free                         |
| Application        | Locomotion controller development  |

## Capabilities

Model‑free RL, as applied in the source paper, provides:

- Development of a **versatile locomotion controller** for [[Wheeled-Legged Robot]]
- Achievement of **efficient and robust locomotion over rough terrains**
- Enablement of **smooth walking–driving mode transitions**

These capabilities are realized without an explicit model of the robot’s dynamics, relying instead on trial‑and‑error interaction and reward shaping.

## Role in System

Model‑free RL is employed to train a locomotion controller that handles varied terrains and mode transitions without requiring an explicit dynamics model. The controller learns robust behaviors directly from simulation or real‑world rollouts, making it suitable for deployment on wheeled‑legged platforms where contact dynamics are complex and difficult to model analytically.

## Relationships

- **Used by**: [[Wheeled-Legged Robot]] (used_by) — the trained controller is integrated into the robot’s software stack.
- **Combined with**: [[Privileged Learning]] (depends_on) — the model‑free training is enhanced by privileged information (e.g., terrain height, friction coefficients) extracted from the simulator during training, which improves sample efficiency and final performance.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Model-Free Reinforcement Learning` --[[implements]] ⚠️--> `Wheeled-Legged Robot`
