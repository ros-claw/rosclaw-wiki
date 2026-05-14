---
id: grpo_group_relative_policy_optimization
title: GRPO (Group Relative Policy Optimization)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:52:19'
last_reinforced: '2026-04-29T20:52:19'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# GRPO (Group Relative Policy Optimization)

**GRPO** (Group Relative Policy Optimization) is a reinforcement learning optimization algorithm, initially introduced in the context of DeepSeek-R1 for fine-tuning language models. It was later adapted by VLN-R1 as the core RL method for reward-driven post-training in visual language navigation (VLN) tasks.

## Overview

GRPO belongs to the family of policy gradient methods and operates by comparing the relative performance of groups of sampled trajectories. Unlike traditional actor-critic approaches that rely on a learned value function, GRPO computes group-based baselines to stabilize training. This design reduces variance and enables efficient optimization with limited reward signal.

In VLN-R1, GRPO is used to fine-tune a vision-language model for navigation by maximizing a reward function based on task success and path efficiency. The algorithm enables the model to learn from sparse reward signals without requiring explicit imitation or human annotations.

## Key Characteristics

- **Group-based baseline**: Computes advantages relative to other sampled trajectories within the same prompt/batch, rather than using a separate critic network.
- **Variance reduction**: The group comparison naturally reduces gradient variance, leading to more stable convergence.
- **Sample efficient**: Particularly effective when the reward signal is sparse or when a large number of trajectories can be sampled in parallel.
- **No separate value function**: Avoids the complexity of training an additional critic, simplifying the training pipeline.

## Relationships

- **Derived from** → DeepSeek-R1: GRPO was first described in the DeepSeek-R1 technical report as the method used to train their reasoning model. VLN-R1 directly adapts this algorithm for navigation tasks.
- **Used by** → VLN-R1: In the VLN-R1 framework, GRPO drives the post-training phase, optimizing the navigation policy via group-relative reward comparisons.

## Usage in VLN-R1

VLN-R1 employs GRPO to fine-tune a pretrained vision-language backbone (e.g., based on LLaVA ⚠️ or similar VLMs) on the VLN-CE benchmark. The reward function typically includes:

- **Success**: whether the agent reaches the target.
- **Path length penalty**: shorter paths are preferred.
- **Collision avoidance**: penalties for invalid steps.

GRPO samples a group of navigation trajectories from the current policy, computes the group-normalized advantages, and updates the policy weights to favor trajectories with higher relative rewards. This process iterates over many episodes until convergence.

## Source

- **Paper**: *VLN-R1: A Vision-Language Navigation Agent with Group Relative Policy Optimization* (arXiv:2506.17221). Contains original description of GRPO as adopted from DeepSeek-R1.

## See Also

- Reinforcement Learning for Robotics ⚠️
- Sim-to-Real Transfer
- Navigation Policy Optimization ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GRPO (Group Relative Policy Optimization)` --extends ⚠️--> `VLN-R1`
- `GRPO (Group Relative Policy Optimization)` --based_on ⚠️--> `VLN-CE`
