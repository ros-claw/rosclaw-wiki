---
id: grpo
title: GRPO
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-30T00:08:46'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.17889.pdf
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# GRPO (Group Relative Policy Optimization)

**GRPO** (Group Relative Policy Optimization) is a reinforcement learning algorithm designed to enhance reasoning consistency and control stability after supervised alignment. It originated from the **DeepSeek-R1** system and is employed as the second-stage training method in [[MobileVLA-R1]]. Additionally, GRPO inspires and is used by **[[VLN-R1]]** for reinforcement fine‑tuning in vision‑language navigation tasks.

## Overview

GRPO was originally developed within the DeepSeek-R1 framework, where it introduced a group‑relative advantage estimation to improve policy learning. In the context of [[MobileVLA-R1]], GRPO is applied in the second training stage. It fine‑tunes the policy initialised by supervised [[Chain-of-Thought Alignment]], focusing on action consistency and robustness in complex, long‑horizon environments. The same group‑relative principle has inspired training approaches in [[VLN-R1]], demonstrating the algorithm’s versatility beyond manipulation.

## Capabilities

- **Group relative policy optimization method** — uses the relative performance of a group of trajectory samples as a baseline, reducing variance without requiring a separate value network.
- **Used for reinforcement fine‑tuning** after supervised alignment, enabling efficient adaptation to task‑specific objectives.
- **Enhances reasoning consistency** after supervised alignment.
- **Improves control stability** during deployment.
- **Reinforces policy** for long‑horizon tasks.

## Origin

GRPO’s core mechanism—computing advantages relative to a group of samples—was first described in the DeepSeek-R1 paper, where it was shown to stabilize training and accelerate convergence. This group‑relative baseline distinguishes GRPO from absolute advantage methods like [[Proximal Policy Optimization]] ⚠️ ⚠️ (PPO).

## Relationships

- **Part of**: [[MobileVLA-R1]]
- **Used by**: [[VLN-R1]]
- **Inspires**: [[VLN-R1]] training
- **Depends on**: [[Chain-of-Thought Alignment]]
- GRPO uses the initialised policy from CoT alignment and further refines it through iterative group‑relative updates.

## Usage in MobileVLA-R1

In the MobileVLA-R1 pipeline, GRPO takes the CoT‑aligned policy and applies gradient updates that compare the relative performance of multiple trajectory samples (the “group”). This group‑relative baseline reduces variance and stabilises training, enabling the robot to execute consistent, robust actions in diverse real‑world settings.

## Usage in VLN-R1

[[VLN-R1]] adapts GRPO for vision‑language navigation, applying the group‑relative advantage formulation to fine‑tune policies that must interpret natural language instructions and plan long‑horizon movement. The shared lineage with DeepSeek-R1 underscores GRPO’s generality as a reinforcement learning optimizer.

For further details, see the original DeepSeek-R1 paper and the related pages on [[Proximal Policy Optimization]] ⚠️ ⚠️ (PPO) for a comparison of group‑relative vs. absolute advantage estimation.

### 自动链接关系
*These relationships were discovered automatically by the heuristic entity linker.*
**Confirmed links:**
- `GRPO` --[[extends]] ⚠️--> `MobileVLA-R1`
- `GRPO` --[[used_by]] ⚠️--> `VLN-R1`