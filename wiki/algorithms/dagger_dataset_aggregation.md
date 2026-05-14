---
id: dagger_dataset_aggregation
title: DAgger (Dataset Aggregation)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:21:08'
last_reinforced: '2026-04-29T21:21:08'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

# DAgger (Dataset Aggregation)

**DAgger** (Dataset Aggregation) is a classic **imitation learning** algorithm designed to train policies by iteratively collecting human expert demonstrations in a closed-loop fashion. It addresses the distribution mismatch problem inherent in behavioral cloning by merging new expert trajectories into the dataset at each iteration, thereby enabling the learner to recover from its own mistakes during training.

## Overview

DAgger was originally proposed by Ross et al. (2011) to overcome the compounding errors of pure behavioral cloning. The algorithm works by:

1. Training an initial policy on a small set of expert demonstrations
2. Deploying the policy in the environment (or simulator) to collect rollouts
3. Querying an expert to label each visited state with the optimal action
4. Aggregating all new state-action pairs into a growing dataset
5. Retraining the policy on the aggregated dataset
6. Repeating steps 2–5 until convergence

This iterative process ensures the policy learns to correct its own induced errors under the actual state distribution it encounters.

## Parameters

- **Type**: imitation learning algorithm
- **Variant**: DAggerFM is a modification of the original DAgger algorithm that introduces a fixed memory budget or curriculum to improve data efficiency and stability.

## Capabilities

- **Train policies with expert interaction**: DAgger leverages an online expert (human or oracle) to provide corrective feedback on the learner's own trajectories, enabling robust policy learning in high-dimensional state spaces.

## Relationships

- *used_by*: **DAggerFM** (DAggerFM modifies DAgger's aggregation scheme to handle fixed memory or a fixed number of expert queries, making it more practical for real-world applications)

DAgger is also a foundational component of many modern imitation learning frameworks and is often compared to behavioral cloning ⚠️ and inverse reinforcement learning ⚠️.

## References

- Ross, S., Gordon, G. J., & Bagnell, D. (2011). *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS.
- Source paper: [arxiv:1806.00047] – introduces DAggerFM as a variant of DAgger.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `DAgger (Dataset Aggregation)` --extends ⚠️--> `DAggerFM`
