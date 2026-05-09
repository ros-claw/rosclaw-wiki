---
id: multi_expert_learning
title: Multi-Expert Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:15:43'
last_reinforced: '2026-04-30T00:15:43'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

# Multi-Expert Learning

## Overview

**Multi-Expert Learning** is an algorithmic framework within the [[MM-Nav]] training pipeline that combines multiple specialized [[Reinforcement Learning]] (RL) experts—each focused on a distinct sub-task—to produce a unified navigation policy. The experts are dynamically balanced according to their individual performance on a given capability, enabling adaptive behavior in complex manipulation and avoidance scenarios.

## Architecture

Multi-Expert Learning employs three dedicated RL experts, each trained independently and then orchestrated by a dynamic weighting mechanism:

| Expert | Role |
|--------|------|
| **Reaching expert** | Specializes in approaching and making contact with target objects. |
| **Squeezing expert** | Focuses on controlled force application or manipulation of the object once reached. |
| **Avoiding expert** | Handles obstacle and collision avoidance during movement. |

## Training Methodology

- **Training data** is collected online from the three RL experts themselves, i.e., using their own interactions with the environment.
- The experts operate with access to **privileged depth information** — ground-truth depth data that may not be available during deployment — to accelerate learning.
- The balancing of expert contributions is **dynamic** and based on the current **individual capability performance** of each expert, measured by a capability evaluation metric.

## Relationship to MM-Nav

Multi-Expert Learning is a core component of the **MM-Nav** (Multi-Modal Navigation) training pipeline. It uses [[Reinforcement Learning]] as the underlying learning paradigm and depends on [[Privileged Depth Information]] for efficient training. The output of this algorithm is a composite policy that integrates the strengths of all three experts.

### Relationships

- `uses` → [[Reinforcement Learning]]
- `uses` → [[Privileged Depth Information]]
- `part_of` → [[MM-Nav]] (training pipeline)

## Advantages

By explicitly decomposing navigation into reaching, squeezing, and avoiding behaviors, Multi-Expert Learning allows each expert to specialize without interference. Dynamic weighting based on performance prevents any single expert from dominating when it is underperforming, resulting in a more robust and adaptable policy compared to monolithic RL training.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multi-Expert Learning` --[[extends]] ⚠️--> `MM-Nav`
