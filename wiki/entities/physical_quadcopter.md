---
id: physical_quadcopter
title: Physical Quadcopter
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:18:35'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1910.09664.pdf
source_type: arxiv_paper
---

---

## Overview

The **Physical Quadcopter** is the unmanned aerial vehicle (UAV) platform used to evaluate the [[SuReAL]] (Supervised Reinforcement Learning with Language) system. It operates in real-world environments, executing natural language instruction-following tasks based solely on first-person visual observations. No specific hardware specifications (e.g., model, processor, sensors) are detailed in the source paper — the platform serves primarily as an embodied testbed for the SuReAL algorithm.

## Capabilities

- **Executes natural language instruction-following tasks** — the quadcopter interprets and carries out commands expressed in free-form natural language (e.g., "fly to the red cone and land").
- **Operates using first-person observations** — all perception is egocentric, relying on an on-board camera feed. No external motion capture or global localization is used during task execution.

## Relationships

- **Uses** — [[SuReAL]]: the quadcopter is controlled by the SuReAL policy, which combines imitation learning and reinforcement learning to map natural language instructions and first-person imagery to low-level flight actions.
- **Depends on** — [[Simulated flight training]] ⚠️: the quadcopter policy is initially trained in simulation before deployment to the physical platform.
- **Depends on** — [[Reinforcement learning policy]] ⚠️: the quadcopter's flight controller relies on a policy refined through reinforcement learning (part of the SuReAL framework) to generalize to real-world conditions.

## Note

> This entity refers to the physical quadcopter platform used in the paper for evaluating SuReAL. Specific hardware details are not provided in the abstract of the source paper (arxiv:1910.09664).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Physical Quadcopter` --[[uses]] ⚠️--> `SuReAL`
- `Physical Quadcopter` --[[depends_on]] ⚠️ ⚠️--> `Simulated flight training`
- `Physical Quadcopter` --[[depends_on]] ⚠️ ⚠️--> `Reinforcement learning policy`