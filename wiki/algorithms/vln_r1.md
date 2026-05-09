---
id: vln_r1
title: VLN-R1
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:51:57'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# VLN-R1

**VLN-R1** is an end-to-end framework for [[Vision-Language Navigation]] that leverages [[Large Vision-Language Models]] ⚠️ ⚠️ (LVLMs) to directly map egocentric video and language instructions to continuous navigation actions. It uses a two-stage training pipeline combining supervised fine-tuning (SFT) and reinforcement fine-tuning (RFT) with a novel reward mechanism and sampling strategy.

The framework is inspired by [[DeepSeek-R1]] and achieves strong performance on the [[VLN-CE]] benchmark.

## Overview

VLN-R1 is a data-efficient, reward-driven post-training approach for embodied navigation. Unlike traditional modular or map-based methods, VLN-R1 processes egocentric video streams end-to-end to produce continuous actions, eliminating the need for discretized action spaces or semantic maps. The base model is a pre-trained LVLM, which is then refined through a two-stage procedure using the [[VLN-Ego dataset]].

## Training

The training procedure consists of two stages:

1. **Supervised Fine-Tuning (SFT)** – The model is first aligned with expert demonstrations by predicting sequences of continuous navigation actions from egocentric video and language instructions. This stage provides a strong initialization for the subsequent reinforcement phase.

2. **Reinforcement Fine-Tuning (RFT)** – The SFT-trained model is further optimized using a GRPO-based ([[GRPO]]) reinforcement learning loop. The reward signal is provided by a **Time-Decayed Reward (TDR)** mechanism that assigns higher importance to actions that contribute more to task completion, weighting future steps appropriately.

**Long-Short Memory Sampling** is used during RFT to efficiently sample trajectories, balancing exploration and exploitation.

## Parameters

| Parameter | Value |
|-----------|-------|
| Base model | [[Large Vision-Language Model]] ⚠️ (LVLM) |
| Training stages | SFT → RFT |
| Reward mechanism | Time-Decayed Reward (TDR) |
| Sampling method | Long-Short Memory Sampling |
| Action space | Continuous navigation actions |

## Capabilities

- End-to-end translation of egocentric video streams into continuous navigation actions.
- Data-efficient, reward-driven post-training requiring only expert demonstrations and the [[VLN-Ego dataset]].
- Strong performance on the [[VLN-CE]] benchmark, demonstrated in the source paper.
- Adopts GRPO-based reinforcement fine-tuning inspired by [[DeepSeek-R1]].

## Relationships

- **Uses**: [[Habitat]] simulator, [[GRPO]], [[Large Vision-Language Models]] ⚠️ ⚠️, [[VLN-Ego dataset]], Long-Short Memory Sampling, Time-Decayed Reward (TDR)
- **Evaluated on**: [[VLN-CE]] benchmark
- **Inspired by**: [[DeepSeek-R1]]

## Source

- arxiv paper: `papers/2506.17221.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLN-R1` --[[based_on]] ⚠️--> `VLN-CE`