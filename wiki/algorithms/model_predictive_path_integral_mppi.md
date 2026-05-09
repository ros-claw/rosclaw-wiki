---
id: model_predictive_path_integral_mppi
title: Model Predictive Path Integral (MPPI)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:37:44'
last_reinforced: '2026-04-29T21:37:44'
supersedes: []
sources:
- papers/2504.19322.pdf
source_type: arxiv_paper
---

## Model Predictive Path Integral (MPPI)

**Model Predictive Path Integral (MPPI)** is a sampling-based [[Model Predictive Control]] ⚠️ (MPC) algorithm that optimizes control sequences by evaluating a cost function over many randomly sampled trajectories. In this implementation, MPPI is integrated zero-shot with a learned forward dynamics model, enabling safe navigation without task-specific tuning or heuristic cost design.

### Parameters

- **Integration**: Zero-shot with a learned forward dynamics model (FDM). The planner does not require any fine-tuning or online adaptation for new environments.
- **Cost Function**: Simplified and heuristic-free. The cost is derived directly from the learned model’s outputs, avoiding manually crafted reward shaping.

### Capabilities

- Optimizes actions for safe navigation in complex, unstructured terrains.
- Leverages a learned mapping between actions, future states, and failure probability, allowing the planner to anticipate and avoid unsafe configurations.

### Relationships

- **`uses`**: [[Learned Perceptive Forward Dynamics Model]] – MPPI relies on this learned model to predict state transitions and failure probabilities.
- **`used_by`**: [[ANYmal]] – the quadruped robot that deploys this MPPI planner for locomotion and navigation tasks.

### Framework

A zero-shot model predictive path integral planning framework that uses the learned forward dynamics model to optimize a simplified cost function. The planner samples action sequences, rolls out the learned model to predict future states and associated risks, and selects the trajectory with the lowest expected cost. This framework eliminates the need for heuristic cost terms by grounding the optimization directly in the learned dynamics and failure predictions.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Model Predictive Path Integral (MPPI)` --[[extends]] ⚠️--> `Learned Perceptive Forward Dynamics Model`
- `Model Predictive Path Integral (MPPI)` --[[implements]] ⚠️--> `ANYmal`
