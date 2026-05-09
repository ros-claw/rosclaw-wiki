---
id: supervised_fine_tuning_sft
title: Supervised fine-tuning (SFT)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:39:26'
last_reinforced: '2026-04-30T00:39:26'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# Supervised Fine-Tuning (SFT)

**Supervised fine-tuning** (SFT) is a training paradigm in which a pretrained model is further trained on a curated dataset of expert demonstrations to align its predictions with desired outputs. In the context of [[Vision-Language Navigation]] (VLN), SFT serves as the initial phase of the two-stage training approach used by [[VLN-R1]], tasking the model to align action sequence text predictions with expert demonstrations.

## Parameters

- **Task**: Align action sequence text predictions with expert demonstrations.

## Capabilities

- SFT serves as the initial training phase for [[VLN-R1]], providing a strong behavioral prior before reinforcement learning.

## Relationships

- **Part of**: [[Two-stage training approach of VLN-R1]] ⚠️ ⚠️ ⚠️
- **Depends on**: [[Supervised learning]] ⚠️ (implicitly used to minimize cross-entropy or similar loss between predicted and expert action sequences)
- **Implements**: [[Behavioral cloning]] ⚠️ ⚠️ at the sequence level (mapping visual observations to action tokens)

## Overview

SFT is typically applied after a base model (e.g., a pretrained vision-language transformer) has been initialized. During SFT, the model is fed <observation, action sequence> pairs from expert human or oracle trajectories. The loss function penalizes deviations from the expert’s choices, effectively imprinting the expert’s decision-making patterns into the model parameters. In [[VLN-R1]], this step is critical because it bootstraps the agent with reasonable behavior before reinforcement learning fine-tunes the policy for long‑horizon reasoning and exploration.

## Relationship with Other Training Stages

| Stage | Method | Purpose |
|-------|--------|---------|
| Stage 1 | **Supervised Fine-Tuning (SFT)** | Align model to expert action sequences |
| Stage 2 | [[Reinforcement Learning]] (RL) | Improve generalization and handle novel environments |

[[VLN-R1]] uses SFT as the first step in its [[Two-stage training approach of VLN-R1]] ⚠️ ⚠️ ⚠️, ensuring the RL stage starts from a competent policy rather than random initialization. The SFT checkpoint is then used as the starting weight for the RL phase.

## See Also

- [[Behavioral cloning]] ⚠️ ⚠️
- [[Vision-Language Navigation]]
- [[VLN-R1]]
- [[Two-stage training approach of VLN-R1]] ⚠️ ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Supervised fine-tuning (SFT)` --[[related_to]] ⚠️--> `VLN-R1` _(wikilink)_
