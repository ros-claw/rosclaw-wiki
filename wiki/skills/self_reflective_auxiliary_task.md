---
id: self_reflective_auxiliary_task
title: Self-Reflective Auxiliary Task
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T01:04:59'
last_reinforced: '2026-04-30T01:04:59'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

## Self-Reflective Auxiliary Task

A **Self-Reflective Auxiliary Task** is a training signal employed during Self-Reflective Post-Training to guide a model toward correct reasoning by explicitly contrasting its predictions with incorrect alternatives. It is one component of the post-training pipeline used in EvolveNav.

### Objective

The primary objective of the self-reflective auxiliary task is to **encourage the model to learn correct reasoning patterns by contrasting them with wrong ones**. Instead of only reinforcing a single correct trajectory, the task exposes the model to both accurate and flawed reasoning chains and trains it to distinguish between them.

### Capabilities

- **Improves reasoning pattern learning** – by forcing the model to evaluate and differentiate between correct and incorrect paths, it internalizes more robust decision-making heuristics.

### Relationships

- **part_of** Self-Reflective Post-Training – the auxiliary task is integrated into the multi-stage post-training process that refines the model’s internal representations.
- **used_in** EvolveNav – this specific post-training technique is applied within the EvolveNav framework to enhance navigation-oriented reasoning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Self-Reflective Auxiliary Task` --uses ⚠️--> `EvolveNav`
