---
id: contrastive_trajectory_sampling
title: Contrastive Trajectory Sampling
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:33:55'
last_reinforced: '2026-04-29T21:33:55'
supersedes: []
sources:
- papers/2505.08712.pdf
source_type: arxiv_paper
---

[[Contrastive Trajectory Sampling]] is a technique used in robot learning, particularly in the context of [[Navigation Diffusion Policy (NavDP)]], to learn a critic value function that evaluates trajectory quality. It leverages **privileged information** available during simulation training to generate contrastive trajectory samples, enabling the policy to distinguish safe, successful trajectories from dangerous or failure-prone ones.

## Purpose

The primary purpose of Contrastive Trajectory Sampling is to **learn a critic value function** that can evaluate the desirability of a trajectory without requiring explicit human annotation. This critic is used to guide the policy toward high-quality actions.

## Capabilities

- Generates **positive trajectory samples** (successful, safe trajectories) and **negative trajectory samples** (failure trajectories, collisions, unsafe states).
- Provides a training signal for the critic network by contrasting positive and negative examples.
- Enables **sample-efficient learning** by leveraging contrastive loss to shape the value landscape.

## Training Procedure

During simulation training, the system first collects trajectories using a navigation policy (e.g., [[NavDP]] ⚠️). For each trajectory, the simulator can access **privileged information** (e.g., ground-truth obstacle positions, future collision states). Using this privileged information, the system labels trajectories as positive (those leading to successful goal arrival without collisions) or negative (those that result in collisions, excessive jerk, or other undesirable outcomes). These labeled trajectories are then used to train a critic (value network) via contrastive loss: the critic is updated to assign higher values to positive trajectories and lower values to negative ones. The trained critic subsequently informs the policy during inference (e.g., by reweighting action proposals).

## Relationships

- **Used by**: [[Navigation Diffusion Policy (NavDP)]] – NavDP employs the learned critic to select the best trajectory from diffusion-generated samples.
- **Depends on**: [[Privileged Information]] ⚠️ – the method relies on privileged simulation state (e.g., true obstacle boundaries, future collisions) to generate ground-truth contrastive labels. After training, the critic generalizes to situations where privileged information is not available.
- **Related concepts**: [[Imitation Learning]], [[Inverse Reinforcement Learning]] ⚠️, [[Contrastive Learning]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Contrastive Trajectory Sampling` --[[related_to]] ⚠️--> `Navigation Diffusion Policy (NavDP)` _(wikilink)_
