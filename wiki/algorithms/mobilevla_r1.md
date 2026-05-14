---
id: mobilevla_r1
title: MobileVLA-R1
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:49:42'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.17889.pdf
source_type: arxiv_paper
---

# MobileVLA-R1

**MobileVLA-R1** is a unified vision-language-action (VLA) framework designed for quadruped robots. It combines a large-scale chain-of-thought dataset with a two-stage training paradigm that first aligns reasoning via supervised learning, then refines behavior through reinforcement learning. The framework explicitly grounds natural-language instructions into continuous control, enabling both reasoning and action execution on mobile robotic platforms.

## Overview

The framework integrates a vision-language backbone with a continuous control policy. It leverages the **MobileVLA-CoT Dataset** — a collection of expert demonstrations annotated with chain-of-thought reasoning traces — to bootstrap reasoning capabilities. A subsequent reinforcement learning stage using **GRPO** further improves reasoning consistency and control stability. This dual-phase approach results in improved long-horizon execution and robustness compared to prior methods.

## Training

MobileVLA-R1 employs a two-stage training paradigm:

- **Stage 1 – Supervised Chain-of-Thought Alignment**: The model is trained on the MobileVLA-CoT Dataset using a supervised learning objective. This stage bridges semantic reasoning and low-level actuation, aligning the model’s reasoning outputs with expert thought processes and action sequences.
- **Stage 2 – GRPO Reinforcement Learning**: GRPO (group relative policy optimization) is applied to refine the policy. This stage enhances reasoning consistency, control stability, and long-horizon performance.

## Capabilities

- Ground natural-language instructions into continuous control commands for quadruped robots.
- Enable explicit reasoning via chain-of-thought, producing interpretable intermediate steps.
- Achieve control stability and robust execution over long horizons.
- Support real-world deployment on quadruped robots.
- Improve performance by approximately 5% over strong baselines on visual-language navigation (VLN) and VLA benchmarks.

## Evaluation

MobileVLA-R1 was evaluated on two major benchmarks:
- **Visual Language Navigation (VLN)**: tasks requiring language-guided navigation in simulated environments.
- **Vision-Language-Action (VLA)**: tasks involving direct instruction following for manipulation and locomotion.

The framework consistently outperformed prior methods, with a roughly 5% improvement in task success and reasoning quality.

## Relationships

- **Uses**: MobileVLA-CoT Dataset, Chain-of-Thought reasoning, GRPO, Quadruped robot platform
- **Depends on**: MobileVLA-CoT Dataset

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MobileVLA-R1` --based_on ⚠️--> `Chain-of-thought reasoning`

## Sources

- Arxiv paper: `papers/2511.17889.pdf` (MobileVLA-R1: Two-Stage Training for Embodied Instruction Following)