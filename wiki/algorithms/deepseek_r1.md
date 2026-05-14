---
id: deepseek_r1
title: DeepSeek-R1
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:52:32'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# DeepSeek-R1

## Overview

DeepSeek-R1 is a large language model that demonstrated effective reasoning through reinforcement fine-tuning. Its core contribution—the Group Relative Policy Optimization (GRPO) method—has inspired downstream algorithms in embodied AI and vision-language navigation. The model showcases a pure RL-based approach to eliciting step-by-step reasoning without extensive human-labeled data, establishing a training paradigm that has been directly adopted by subsequent systems.

## Description

DeepSeek-R1 was developed to improve the reasoning capabilities of LLMs without relying on large-scale supervised fine-tuning. Instead, it applies reinforcement learning directly to the model’s output generation, using a carefully designed reward scheme that rewards correct reasoning chains. The key innovation is the **GRPO** algorithm, which stabilizes training by grouping rollouts and computing advantages relative to group means rather than using a separate value network.

This approach is directly adopted by VLN-R1, which adapts GRPO to train multimodal agents for vision-and-language navigation tasks. The training method demonstrated by DeepSeek-R1—GRPO-based reinforcement fine-tuning—is the foundational technique replicated across multiple embodied reasoning domains.

## Capabilities

- **Reasoning through reinforcement fine-tuning**: DeepSeek-R1 shows that pure RL, without extensive human-labeled reasoning data, can elicit step-by-step logical deduction.
- **GRPO-based training approach**: The model demonstrates a complete, verified pipeline for applying the GRPO algorithm to elicit reasoning in language models. This capability serves as a proof-of-concept for transferring the technique to modalities beyond text, such as vision-language navigation.
- **Source of GRPO**: The GRPO method is the core algorithmic contribution and has been reused in subsequent embodied AI systems.
- **Inspiration for embodied reasoning**: By demonstrating RL-based reasoning in language, DeepSeek-R1 opened the door to similar techniques in robotic decision-making, including the adoption of GRPO by VLN-R1 and others.

## Relationships

| Relation | Entity | Notes |
|----------|--------|-------|
| inspires | GRPO | GRPO is the reinforcement learning algorithm introduced within DeepSeek-R1. |
| inspires | VLN-R1 | VLN-R1 adopts GRPO for training navigation policies, directly inspired by the DeepSeek-R1 training paradigm. |

- **inspires**: GRPO, VLN-R1  
- **depends_on**: Basic LLM architecture, reinforcement learning from human feedback (RLHF) concepts

## References

- Source paper: `papers/2506.17221.pdf` (arXiv)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**
- `DeepSeek-R1` --inspires ⚠️--> `VLN-R1` *(updated from extends)*