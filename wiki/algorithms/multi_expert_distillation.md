---
id: multi_expert_distillation
title: Multi-expert Distillation
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:37:10'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

# Multi-expert Distillation

**Multi-expert Distillation** is a training framework for [[Embodied AI]] that trains terrain-specific expert policies and distills them into a unified policy using [[DAgger]], followed by [[Reinforcement Learning Fine-tuning]]. This approach produces a single controller capable of robust generalization across diverse real-world terrains without requiring a single, large expert network.

## Overview

Multi-expert distillation trains terrain-specific experts and distills them into a unified policy using DAgger, followed by RL fine-tuning. This yields a single foundation policy that synthesizes multi-terrain skills and generalizes robustly to unseen real-world environments.

## Parameters

- **Method**: Distillation using [[DAgger]] (Dataset Aggregation)
- **Input**: [[Depth images]] ⚠️ ⚠️
- **Output**: Unified foundation policy

## Capabilities

- Train terrain-specific expert policies, each optimized for a single surface or obstacle type
- Distill multiple expert policies into a unified foundation policy using DAgger
- Synthesize multiple terrain-specific skills into a single unified controller
- Generalize robustly to unseen real-world terrains
- Fine-tune the distilled policy via RL on a broader terrain set, including real-world 3D scans

## Process

1. **Expert training**: For each terrain class (e.g., grass, gravel, stairs), a separate expert policy is trained via RL with full state information and privileged rewards.
2. **Distillation**: DAgger iteratively collects rollouts from the student policy, queries the appropriate expert (based on terrain label), and trains the student on the resulting dataset. This yields a single policy that approximates the behavior of all experts.
3. **RL fine-tuning**: The distilled policy is further refined with model-free RL on a diverse set of terrains, including high-fidelity scans of real-world environments, to compensate for distribution shift and improve robustness.

## Relationships

- **Uses** `01-uses` :: [[DAgger]], [[Reinforcement Learning Fine-tuning]]
- **Depends on** `01-depends_on` :: [[Terrain-specific expert policies]] ⚠️, [[Depth images]] ⚠️ ⚠️
- **Part of** `01-part_of` :: [[Agile Locomotion]]

## Source

- arxiv paper: [[2505.11164]] ⚠️ (Multi‑expert Distillation for Scalable Locomotion in Unstructured Environments)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multi-expert Distillation` --[[based_on]] ⚠️--> `Embodied AI`