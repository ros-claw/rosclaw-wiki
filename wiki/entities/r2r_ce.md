---
id: r2r_ce
title: R2R-CE
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:34'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.01550.pdf
- papers/2406.04882.pdf
source_type: arxiv_paper
---

## R2R-CE

**R2R-CE** (Room-to-Room with Continuous Environments) is a navigation benchmark for evaluating embodied agents that follow natural language instructions in continuous, unconstrained 3D spaces. It extends the original Room-to-Room (R2R) dataset by replacing discrete graph-based action spaces with continuous movement (translation and rotation), demanding realistic obstacle avoidance, spatial reasoning, and long-horizon planning in indoor scenes.

R2R-CE belongs to the domain of **embodied navigation** and is closely related to R2R, VLN-CE, Habitat ObjNav, and DDN.

### Key Features
- Continuous action space (movement in meters/degrees, no teleportation)
- Natural language instructions paired with trajectories in 3D scans
- Evaluates both planning and low-level control in collision-free navigation
- Metrics include Success Rate (SR), Oracle Success Rate (OSR), and Path Length (PL) penalties

### Methods Using R2R-CE

**InstructNav** is the first method to complete the R2R-CE task in a zero-shot manner, using the benchmark as a testbed for instruction-driven navigation without prior training on the dataset.

**NavForesee** implements a model trained on R2R-CE to perform foresight‑based trajectory planning. The benchmark provides the instruction‑trajectory pairs and simulator interface used for both training and evaluation.

Both approaches demonstrate the flexibility of R2R-CE as a standard evaluation suite for embodied navigation agents.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `R2R-CE` ––used_by ⚠️ ⚠️––> `InstructNav`
- `R2R-CE` ––used_by ⚠️ ⚠️––> `NavForesee`
- `R2R-CE` ––related_to ⚠️ ⚠️ ⚠️––> `VLN-CE`
- `R2R-CE` ––related_to ⚠️ ⚠️ ⚠️––> `Habitat ObjNav`
- `R2R-CE` ––related_to ⚠️ ⚠️ ⚠️––> `DDN`