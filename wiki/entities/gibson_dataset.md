---
id: gibson_dataset
title: Gibson dataset
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-30T00:13:54'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2502.19024.pdf
- papers/2312.03275.pdf
source_type: arxiv_paper
---

# Gibson Dataset

The **Gibson Dataset** is a dataset of real-world indoor scenes used for navigation tasks in [[Habitat]]. It provides photo-realistic indoor environments and a connectivity graph that serves as spatial priors for navigation and planning tasks in embodied AI research.

## Description

The Gibson Dataset consists of real-world indoor environments scanned and reconstructed to support embodied AI agents. It is widely used as a benchmark and training resource for navigation tasks, especially within the [[Habitat]] simulation platform.

## Capabilities

- Provides a connectivity graph for spatial priors, enabling agents to reason about navigable paths and scene structure.
- Provides photo-realistic indoor environments for training and evaluation of navigation agents.

## Relationships

- Used by [[GVNav]] for ground-truth-based navigation evaluation.
- Used in [[VLFM]] evaluation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Gibson dataset` --[[uses]] ⚠️--> `GVNav`