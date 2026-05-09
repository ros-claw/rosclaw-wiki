---
id: model_free_learning
title: Model-Free Learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:36:29'
last_reinforced: '2026-04-30T04:36:29'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

## Model-Free Learning

**Model-Free Learning** is a class of reinforcement learning and control approaches that learns sensor-to-action mappings directly from experience, without explicitly modeling the world's dynamics or terrain properties. In the context of legged locomotion and navigation, this enables policies such as [[ViNL]] (Visual Navigation and Locomotion) to map visual observations to walking commands end-to-end.

### Definition
A learning approach that uses neural networks to map sensors directly to actions, trained end-to-end. No explicit model of world dynamics (e.g., terrain geometry, friction, or dynamics predictions) is used. The policy learns to generalize across environments purely from data, often through trial-and-error or imitation.

### Capabilities
- Learn sensor-to-action mappings directly without explicit terrain models
- Enable zero-shot or few-shot generalization to novel terrains
- Simplify system architecture by removing the need for separate model-building or simulator-tuning stages

### Relationships

| Relationship | Entity | Notes |
|--------------|--------|-------|
| **Used by** | [[Visual Locomotion Policy]] ⚠️ | Core learning paradigm for end-to-end locomotion control |
| **Used by** | [[Visual Navigation Policy]] | Navigation commands derived directly from visual input without world model |
| **Used by** | [[ViNL]] | Combines model‑free locomotion and navigation in one policy |
| **Contrasts with** | [[model-based control]] ⚠️ | Model‑based methods build explicit dynamics or terrain models (e.g., privileged terrain maps) for planning |
| **Contrasts with** | [[privileged terrain maps]] ⚠️ | Model‑free avoids the need for precomputed terrain representations |

### Source
Derived from the work on ViNL (arXiv:2210.14791), which demonstrates model‑free policies for visually‑guided locomotion.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Model-Free Learning` --[[related_to]] ⚠️--> `ViNL` _(wikilink)_
