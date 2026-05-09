---
id: 1x_humanoid_dataset
title: 1X Humanoid Dataset
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:33:50'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

# 1X Humanoid Dataset

The **1X Humanoid Dataset** is a dataset of high-dimensional humanoid control trajectories used to evaluate the scaling properties of the [[UniWM]] model. It originates from the 1X Technologies humanoid platform and is part of broader [[Humanoid control datasets]] ⚠️ ⚠️ collections.

## Description

This dataset provides trajectories of a full-body humanoid robot performing various motor tasks, including navigation behaviors. It is specifically designed to test the capability of universal world models (such as UniWM) to generalize to high-dimensional action and observation spaces. In particular, the dataset is used to demonstrate UniWM's scalability to humanoid control and to evaluate the scaling of navigation methods when applied to complex humanoid platforms. The dataset includes real-world demonstration data, sensor readings, and control commands, making it suitable for both imitation learning and reinforcement learning experiments.

## Relationships

- **Part of** [[Humanoid control datasets]] ⚠️ ⚠️
- **Used by** [[UniWM]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `1X Humanoid Dataset` --[[uses]] ⚠️--> `UniWM`