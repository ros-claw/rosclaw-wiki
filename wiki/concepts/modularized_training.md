---
id: modularized_training
title: Modularized Training
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:39:37'
last_reinforced: '2026-04-30T02:39:37'
supersedes: []
sources:
- papers/2104.10674.pdf
source_type: arxiv_paper
---

# Modularized Training

**Modularized Training** is a concept in hierarchical agent design where separate components of a system—such as high-level policies and low-level policies—are trained independently rather than jointly. By decoupling the training of these modules, the approach improves both performance and sample efficiency, particularly in tasks requiring both reasoning and motor imitation.

## Overview

In hierarchical systems, a [[Hierarchical Agent]] ⚠️ often consists of a high-level policy (responsible for abstract reasoning or task planning) and a low-level policy (executing fine-grained actions). Traditional joint training can be costly and unstable due to the complex interaction between levels. **Modularized Training** breaks this coupling: each module is optimized using its own reward structure or loss function, often leveraging distinct training techniques (e.g., reinforcement learning for the high level, behavioral cloning for the low level). This separation simplifies credit assignment and enables faster convergence.

## Capabilities

- **Decouples reasoning and imitation**: The high-level policy can focus on long-term strategy while the low-level policy learns precise replication.
- **Improves sample efficiency**: Independent training reduces the overall number of environment interactions needed.
- **Enables modular reuse**: Trained low-level skills can be transferred to new high-level tasks without retraining.

## Relationships

- **Used by**: [[Hierarchical Cross-Modal (HCM) Agent]] — This agent architecture demonstrates modularized training to combine visual reasoning with motor imitation.
- **Supports**: [[Imitation Learning]] and [[Reinforcement Learning]] — These techniques are commonly used for the low-level and high-level modules respectively.
- **Depends on**: [[Hierarchical Reinforcement Learning]] for the overarching framework, and [[Behavioral Cloning]] ⚠️ for low-level skill acquisition.

## Description

Modularized training involves training separate components of a system (e.g., high-level policy and low-level policy) independently, which can improve performance and sample efficiency. The modular approach also facilitates composability: once a low-level policy is trained for a specific skill repertoire, it can be reused across multiple high-level reasoning modules.

## See Also

- [[End-to-End Training]] ⚠️
- [[Hierarchical Imitation Learning]] ⚠️
- [[Cross-Modal Embodied Agents]] ⚠️

> *Source: arxiv paper 2104.10674*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Modularized Training` --[[related_to]] ⚠️--> `Hierarchical Reinforcement Learning` _(wikilink)_
