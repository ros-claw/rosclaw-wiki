---
id: qwen25_vl_3b
title: Qwen2.5-VL-3B
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:02:01'
last_reinforced: '2026-04-30T00:02:01'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

# Qwen2.5-VL-3B

## Overview

**Qwen2.5-VL-3B** is a Large Vision-Language Model (LVLM) with 3 billion parameters, part of the Qwen2.5-VL series developed by Alibaba Cloud. In the context of embodied navigation, it serves as the backbone of the SeeNav-Agent and is fine-tuned using a novel post-training algorithm called Step Reward Group Policy Optimization (SRGPO). Post-training with SRGPO significantly boosts its navigation success rate, achieving state-of-the-art performance on the EmbodiedBench Navigation ⚠️ benchmark.

## Key Capabilities

- **Vision-Language Understanding**: Combines visual and textual inputs to reason about navigation tasks in complex environments.
- **Step-level Reinforcement Fine-Tuning**: The fine-tuning procedure (SRGPO) optimizes the model at every step of a trajectory, leading to more robust and accurate navigation decisions.
- **Performance Improvement**: After SRGPO, Qwen2.5-VL-3B surpasses the previous best LVLM by 5.6 percentage points on EmbodiedBench Navigation (72.3% vs. 66.7%).

## Post-training Result

After applying Step Reward Group Policy Optimization (SRGPO) post-training, Qwen2.5-VL-3B achieved a **navigation success rate of 72.3%** on the EmbodiedBench Navigation benchmark. This result represents a 5.6% absolute improvement over the best prior LVLM, highlighting the effectiveness of step-level reward shaping in fine-tuning large vision-language models for embodied tasks.

## Relationships

| Relation       | Entity                               | Type                    |
|----------------|--------------------------------------|-------------------------|
| used_in        | SeeNav-Agent                     | Embodied navigation system |
| trained_with   | Step Reward Group Policy Optimization (SRGPO) | Reinforcement fine-tuning algorithm |

- Qwen2.5-VL-3B is used as the core perception-and-planning model inside SeeNav-Agent.
- It depends on Step Reward Group Policy Optimization (SRGPO) for post-training to achieve high navigation success rates.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Qwen2.5-VL-3B` --uses ⚠️ ⚠️--> `SeeNav-Agent`
- `Qwen2.5-VL-3B` --uses ⚠️ ⚠️--> `Step Reward Group Policy Optimization (SRGPO)`
