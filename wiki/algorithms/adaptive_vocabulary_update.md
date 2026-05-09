---
id: adaptive_vocabulary_update
title: Adaptive Vocabulary Update
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:45:23'
last_reinforced: '2026-04-30T03:45:23'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

# Adaptive Vocabulary Update

**Adaptive Vocabulary Update** is an algorithm that enables open-vocabulary navigation by dynamically extending or modifying the set of recognizable semantic labels during inference. It is a core component of the [[MSGNav]] system.

## Overview

Traditional navigation systems are limited to a fixed set of object categories or commands seen during training. Adaptive Vocabulary Update overcomes this by allowing the vocabulary of the navigation agent to expand in real time. This capability is essential for open-vocabulary tasks where the agent must understand and act upon novel object names or spatial relations without retraining.

## Role in MSGNav

As part of [[MSGNav]], the algorithm maintains an updatable vocabulary that interacts with the system’s perception and planning modules. When a new label is encountered (e.g., from a user command or visual input), the vocabulary is updated to include it. This updated vocabulary is then used for grounding the instruction in the current environment, enabling zero-shot generalization to unseen categories.

## Relationship with Other Components

- **Part of** → [[MSGNav]]  
- **Enables** → [[Open Vocabulary]] ⚠️ navigation  
- **Depends on** → The underlying feature extractor and semantic similarity metric (typically from a [[Vision-Language Model]] or [[CLIP]])

## References

- Source paper: *[MSGNav: Multi-Scale Graph Navigation with Adaptive Vocabulary Update](https://arxiv.org/abs/2511.10376)* (arxiv:2511.10376)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Adaptive Vocabulary Update` --[[extends]] ⚠️ ⚠️--> `MSGNav`
- `Adaptive Vocabulary Update` --[[extends]] ⚠️ ⚠️--> `CLIP`
