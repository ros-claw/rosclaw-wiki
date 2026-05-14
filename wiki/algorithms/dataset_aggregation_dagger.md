---
id: dataset_aggregation_dagger
title: Dataset Aggregation (DAgger)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:34:35'
last_reinforced: '2026-04-29T20:34:35'
supersedes: []
sources:
- papers/2603.16166.json
source_type: arxiv_paper
---

# Dataset Aggregation (DAgger)

**Dataset Aggregation (DAgger)** is a popular imitation learning algorithm designed to address the covariate shift problem in behavioral cloning. Instead of relying solely on a fixed dataset of expert demonstrations, DAgger iteratively collects new data under the current policy's distribution, queries the expert for corrective actions, and aggregates this data into the training set. This process improves the policy's robustness by exposing it to states it is likely to encounter during deployment.

## Capabilities

- Used as a training strategy to improve policy performance in imitation learning settings.
- Employs a **two-stage training** pipeline: initial supervision from expert demonstrations, followed by iterative online data collection and retraining.

## Usage

DAgger is applied in the training of the Spatial-Temporal Aware Transformer (START) model as part of its learning framework. START uses DAgger to iteratively refine its policy by collecting rollouts and querying expert feedback, enabling the model to generalize better to novel spatial-temporal scenarios.

## Relationship Annotations

- **Spatial-Temporal Aware Transformer (START)** → *implements* → Dataset Aggregation (DAgger)
- Dataset Aggregation (DAgger) → *used_in* → Spatial-Temporal Aware Transformer (START)

## Related Concepts

- Imitation Learning
- Behavioral Cloning ⚠️
- Covariate Shift ⚠️
- Interactive Imitation Learning ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Dataset Aggregation (DAgger)` --extends ⚠️--> `Spatial-Temporal Aware Transformer (START)`
