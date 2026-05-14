---
id: r2r_room_to_room
title: R2R (Room-to-Room)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:37:28'
last_reinforced: '2026-04-30T01:37:28'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

# R2R (Room-to-Room)

**R2R (Room-to-Room)** is a benchmark dataset and task for Vision-and-Language Navigation (VLN). It evaluates an agent’s ability to follow descriptive natural language instructions to navigate from one room to another within real-world environments.

## Overview

The R2R dataset was introduced in the paper *"Vision-and-Language Navigation: Interpreting Visually-Grounded Navigation Instructions in Real Environments"* (arXiv 2308.12587). It is one of the foundational benchmarks in the VLN Benchmarks ⚠️ ⚠️ ⚠️ family, providing a standardized evaluation protocol for agents that must combine visual perception and language understanding.

## Task Description

- **Task type**: Vision-and-Language Navigation with descriptive instructions.
- **Dataset type**: Benchmark (train/validation/test splits with ground-truth trajectories).
- **Input**: A natural language instruction (e.g., *"Walk past the kitchen table, turn left at the sofa, and stop at the doorframe"*) paired with a starting viewpoint in a photorealistic Matterport3D ⚠️ ⚠️ environment.
- **Output**: A sequence of navigation actions (move forward, turn left/right, stop) that completes the described route.
- **Evaluation metrics**: Success rate, path length, and task completion improvements over baseline models.

## Capabilities

| Capability | Description |
|-----------|-------------|
| Evaluates agent ability to follow natural language instructions | The agent must parse spatial language, ground it to visual observations, and execute a coherent path. |

## Relationships

- `part_of` VLN Benchmarks ⚠️ ⚠️ ⚠️ — R2R is a core component of the VLN evaluation suite.
- `implements` Visually-Grounded Instruction Following ⚠️ — The task structure requires grounding language to visual features.
- `depends_on` Matterport3D ⚠️ ⚠️ — The dataset is built on Matterport3D environments.
- `used_by` Transformer-based VLN Models ⚠️ — Many models (e.g., VLN-BERT, HAMT) are evaluated on R2R.

## Significance

R2R has set the standard for indoor VLN research. Its descriptive instructions (as opposed to imperative commands) challenge models to handle spatial prepositions, landmarks, and sequential reasoning. The benchmark continues to drive progress in embodied AI instruction following.

> *For further details, see the original paper and the VLN Benchmarks ⚠️ ⚠️ ⚠️ page.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `R2R (Room-to-Room)` --related_to ⚠️--> `Vision-and-Language Navigation`
