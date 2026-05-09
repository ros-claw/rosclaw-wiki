---
id: online_expert_guided_reinforcement_learning
title: Online Expert-Guided Reinforcement Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T23:59:22'
last_reinforced: '2026-04-29T23:59:22'
supersedes: []
sources:
- papers/2601.08665.pdf
source_type: arxiv_paper
---

# Online Expert-Guided Reinforcement Learning

**Online Expert-Guided Reinforcement Learning** is a post-supervised learning algorithm that refines a pretrained navigation model by combining [[Reinforcement Learning]] with expert demonstrations. Its objective is to acquire robust self-explored navigation behaviors beyond what pure [[Imitation Learning]] can provide.

## Capabilities

- Allows the model to surpass the performance ceiling of imitation learning.
- Enables self-explored robust behaviors that generalize to unseen environments.

## Training Strategy

After pretraining on the [[Nav-AdaCoT-2.9M]] dataset, the model (part of the [[VLingNav]] training pipeline) undergoes online RL with a learned [[Reward Function]] ⚠️ guided by expert priors. This phase refines behavior beyond the initial supervised imitation, enabling the agent to discover more effective navigation policies through trial and error while staying anchored by expert knowledge.

## Parameters

| Parameter | Value |
|-----------|-------|
| Training stage | Post-supervised learning |
| Guidance | Expert demonstrations |
| Objective | Acquire robust self-explored navigation behaviors beyond imitation learning |

## Relationships

- **Part of:** [[VLingNav]] training pipeline (implements the post-supervised refinement stage).
- **Depends on:** [[Reinforcement Learning]] (core learning paradigm), [[Expert Demonstrations]] ⚠️ (provides priors and reward shaping).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Online Expert-Guided Reinforcement Learning` --[[extends]] ⚠️--> `VLingNav`
