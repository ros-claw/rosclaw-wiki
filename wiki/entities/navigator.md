---
id: navigator
title: Navigator
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:46:03'
last_reinforced: '2026-04-30T00:46:03'
supersedes: []
sources:
- papers/2412.08467.pdf
source_type: arxiv_paper
---

# Navigator

**Navigator** is a **language-guided navigation model** that learns to follow natural language instructions to navigate through environments. It is a core component of the [[Self-Refining Data Flywheel (SRDF)]] pipeline.

## Overview

The Navigator model takes an instruction (e.g., "go to the kitchen and pick up the apple") and generates a trajectory — a sequence of actions — to execute the instruction. It is trained on [[instruction-trajectory pairs]] ⚠️ ⚠️ and employs a data filtering mechanism that enables a self-refining flywheel: the model itself helps curate higher-quality training data, leading to iterative improvement.

## Capabilities

- **Language-guided navigation**: performs goal-directed movement based on textual commands.
- **Data filtering for self-refining flywheel**: the Navigator participates in selecting the most informative instruction-trajectory pairs to be added back into its training pool, driving a cycle of automatic improvement.

## Training

The training process follows a two-stage strategy:

1. **Initial data pool** – the model is first trained on a large, possibly noisy dataset of instruction-trajectory pairs.
2. **Refined data** – after initial training, the Navigator is used to filter and score candidate trajectories; only high-confidence or high‑reward pairs are retained for further fine‑tuning.

This iterative approach yields a steady increase in performance without manual data cleaning.

## Performance

On the Room-to-Room (R2R) benchmark, the Navigator achieves an **SPL of 78%** when trained within the SRDF framework.

## Relationships

- [[Navigator]] **depends on** [[instruction-trajectory pairs]] ⚠️ ⚠️ for training.
- [[Navigator]] **implements** language-guided navigation.
- [[Navigator]] **is used by** [[Self-Refining Data Flywheel (SRDF)]].

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Navigator` --[[uses]] ⚠️--> `Self-Refining Data Flywheel (SRDF)`
