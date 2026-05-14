---
id: navillm
title: NaviLLM
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:05:31'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2312.02010.pdf
source_type: arxiv_paper
---

# NaviLLM

## Summary

NaviLLM is the first generalist model for embodied navigation, adapting Large Language Models via schema-based instruction to unify diverse navigation tasks and datasets into a single sequence generation framework.

## Overview

NaviLLM is a generalist model designed specifically for Embodied Navigation tasks. It adapts Large Language Models to the challenges of physical navigation by introducing **schema-based instruction**, a novel approach that casts a wide variety of navigation tasks into unified sequence generation problems. This enables the model to be trained jointly across multiple datasets and to generalize to unseen tasks such as embodied question answering and 3D captioning. NaviLLM supersedes task-specific agents ⚠️ ⚠️ by providing a single model that handles multiple navigation benchmarks.

## Capabilities

- **Unified task handling**: NaviLLM can perform diverse embodied navigation tasks (e.g., vision-and-language navigation, object goal navigation, embodied question answering, 3D captioning) using a single schema-based instruction framework.
- **State-of-the-art performance**: Achieves new best results on the **CVDN** dataset (29% improvement in goal progress), as well as on **SOON** and **ScanQA** benchmarks.
- **Zero-shot generalization**: After training, NaviLLM can tackle tasks it has never seen before, such as embodied question answering from visual environments and 3D scene captioning, demonstrating strong generalizability to unseen tasks.

## Parameters

| Parameter      | Value                                    |
|----------------|------------------------------------------|
| Base Model     | Large Language Model (architecture unspecified in original paper) |
| Task Type      | Embodied Navigation                      |
| Method         | Schema-based Instruction                 |

The backbone is an off-the-shelf pre-trained Large Language Model, augmented with a perception module that maps visual observations into the LLM's embedding space.

## Relationships

- **uses** → Large Language Models — the core reasoning engine.
- **uses** → Schema-based Instruction — the method for unifying task definitions.
- **implements** → Embodied Navigation — NaviLLM directly solves navigation tasks in simulation and real environments.
- **depends_on** → Schema-based Instruction — the key innovation enabling joint training across tasks.
- **supersedes** → task-specific agents ⚠️ ⚠️ — replaces separate models for each navigation benchmark with a single generalist architecture.
- **depends_on** → Vision-Language Pretraining ⚠️ — achieves cross-modal understanding via schema-based instruction.

## Source

- arXiv paper: "NaviLLM: A Unified Model for Embodied Navigation via Schema-based Instruction" (2312.02010).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `NaviLLM` --based_on ⚠️--> `Schema-based Instruction`