---
id: privileged_learning
title: Privileged Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:42:19'
last_reinforced: '2026-04-29T21:42:19'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

## Overview

**Privileged Learning** is a [[Teacher-Student]] ⚠️ training paradigm for [[Locomotion Control]] ⚠️ that provides a policy with access to privileged state information (e.g., [[Terrain Properties]] ⚠️, ground friction, contact forces) during training, but only uses on-board sensor observations during deployment. This improves robustness by enabling the controller to infer hidden environmental conditions from available sensory data.

## Purpose

Privileged learning allows the locomotion controller to access state information during training that is not available during deployment, improving robustness. By learning to map privileged signals to sensor-based features, the controller can generalize to unseen terrains without explicit terrain classification.

## Parameters

| Parameter | Value |
|-----------|-------|
| Training paradigm | Teacher-student |
| Use case | Locomotion control |

## Capabilities

- Provide privileged information during training (e.g., terrain properties, ground reaction forces)
- Enable the controller to infer terrain from onboard sensors at runtime (e.g., [[IMU]] ⚠️, joint encoders, foot contact sensors)

## Relationships

- **Used by**: [[Wheeled-Legged Robot]]
- **Depends on**: [[Model-Free Reinforcement Learning]] (as the underlying algorithm for the teacher and student policies)

---

*Based on [[ArXiv:2405.01792]] ⚠️ — "Wheeled-Legged Robot Locomotion via Privileged Learning".*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Privileged Learning` --[[implements]] ⚠️--> `Wheeled-Legged Robot`
- `Privileged Learning` --[[extends]] ⚠️--> `Model-Free Reinforcement Learning`
