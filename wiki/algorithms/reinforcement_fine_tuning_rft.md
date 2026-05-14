---
id: reinforcement_fine_tuning_rft
title: Reinforcement Fine-Tuning (RFT)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-30T00:04:18'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02631.pdf
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# Reinforcement Fine-Tuning (RFT)

## Overview

**Reinforcement Fine-Tuning (RFT)** is a post-training method for Large Vision-Language Models (LVLMs) used in navigation tasks. It applies reinforcement learning to fine-tune LVLMs specifically for improving planning capability in Visual Language Navigation (VLN) agents. RFT enables step-level policy optimization and provides dense reward signals for fine-tuning, bridging the gap between generic pre-training and task-specific navigation reasoning. RFT also forms the second phase of the two-stage training approach used in VLN-R1, where reward-driven optimization follows an initial imitation learning stage.

## Background

Reinforcement Fine-Tuning (RFT) is a post-training approach that applies reinforcement learning to fine-tune LVLMs for specific tasks. It addresses the limitations of supervised fine-tuning by incorporating reward signals derived from the navigation environment, allowing the model to explore and optimize its behavior at a granular, step-level granularity. RFT builds on the success of reinforcement learning from human feedback (RLHF) but adapts it to the continuous, action-oriented world of embodied navigation.

## Variants

Reinforcement Fine-Tuning encompasses several algorithmic instantiations:

- **GRPO** – Group Relative Policy Optimization, a baseline RFT method that groups trajectories to estimate advantages.
- **GiGPO ⚠️ ⚠️** – Generalized Group Policy Optimization, an extension of GRPO with more flexible advantage estimation.
- **SRGPO ⚠️ ⚠️** – Step Reward Group Policy Optimization, proposed as an improvement over GRPO and GiGPO specifically for VLN tasks. SRGPO introduces step-level dense rewards derived from navigation sub-goals, enabling finer-grained policy updates.
- **Time-Decayed Reward (TDR) mechanism** – An enhancement to the reward structure that applies a decay factor over time, encouraging the agent to complete tasks efficiently by discounting rewards for later steps. This mechanism is particularly useful in long-horizon navigation and is employed in the RFT training of VLN-R1.

SRGPO is highlighted as a key improvement that addresses the sparse reward problem in long-horizon navigation, making it well-suited for agents like SeeNav-Agent. The TDR mechanism complements this by adding temporal incentives, further improving convergence and task success.

## Capabilities

- **Second training phase for VLN-R1**: RFT serves as the reward-driven optimization stage after supervised fine-tuning, enabling the agent to move beyond imitation and explore more optimal policies.
- **Step-level policy optimization**: RFT methods, particularly SRGPO, allow the agent to learn effective actions at each step rather than only receiving terminal rewards.
- **Dense reward signals**: By decomposing the navigation task into sub-goals (SRGPO) or applying time-decayed rewards (TDR), RFT provides more frequent and informative feedback during training, accelerating convergence and improving final task success rates.
- **Improves planning capability**: Directly optimizes the LVLM’s policy for the downstream navigation objective, leading to better generalization and robustness.

## Relationships

- **`implements`** -> Reinforcement Learning as a training paradigm.
- **`used_in`** -> SeeNav-Agent (the VLN agent that employs SRGPO for fine-tuning) and VLN-R1 (which uses RFT as the second stage of its two-stage training approach).
- **`has_instance`** -> SRGPO ⚠️ ⚠️, GRPO, GiGPO ⚠️ ⚠️, and Time-Decayed Reward (TDR) (specific algorithms or mechanisms).
- **`depends_on`** -> LVLM ⚠️ (Large Vision-Language Model as the base architecture being fine-tuned).
- **`improves_upon`** -> Supervised Fine-Tuning ⚠️ by using RL-based objectives instead of imitation learning.
- **`part_of`** -> The two-stage training approach of VLN-R1 (RFT follows initial supervised fine-tuning).

## References

- Source paper: *arxiv 2512.02631* – details the SRGPO algorithm and its evaluation on navigation benchmarks.
- Source paper: *arxiv 2506.17221* – introduces the VLN-R1 two-stage training framework including the Time-Decayed Reward (TDR) mechanism within RFT.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Reinforcement Fine-Tuning (RFT)` --extends ⚠️--> `SeeNav-Agent`
- `Reinforcement Fine-Tuning (RFT)` --part_of ⚠️--> `VLN-R1`