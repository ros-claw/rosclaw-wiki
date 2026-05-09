---
id: vln_ce_datasets
title: VLN-CE datasets
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:01:25'
last_reinforced: '2026-04-29T21:01:25'
supersedes: []
sources:
- papers/2404.01943.pdf
source_type: arxiv_paper
---

# VLN-CE Datasets

The **VLN-CE datasets** (Vision-Language Navigation in Continuous Environments) are a collection of benchmarks and simulation environments designed to evaluate **continuous** vision-language navigation (VLN) agents in large-scale 3D environments. Unlike discrete VLN datasets (e.g., Room-to-Room), VLN-CE requires agents to execute free-form motion in realistic 3D reconstructions, making the task significantly more challenging and closer to real-world deployment.

## Overview

VLN-CE datasets are part of the broader [[VLN-CE challenge]] ⚠️ ⚠️ ⚠️. They provide a standardized benchmark that includes:

- **Continuous action spaces**: agents move with velocity and rotation commands rather than graph-based node transitions.
- **Realistic 3D environments**: built from Matterport3D, Habitat-Matterport 3D, or Gibson scans.
- **Instruction-following**: paired navigation instructions and ground-truth trajectories.
- **Evaluation metrics**: success rate, path length weighted success (SPL), and execution efficiency.

## Relationship

- **Used by**: The [[lookahead VLN model]] ⚠️ ⚠️ (and many other continuous VLN agents) for training and evaluation.
- **Part of**: The [[VLN-CE challenge]] ⚠️ ⚠️ ⚠️, a benchmark series that tracks progress in continuous VLN.
- **Depends on**: The [[Habitat Simulator]] platform for rendering and physics; the datasets are typically released as a set of episodes compatible with [[Habitat-Lab]] ⚠️.

## Capabilities

- Provides a reproducible benchmark for **continuous vision-language navigation** in complex, photo-realistic 3D environments.
- Enables head-to-head comparison of models that operate in continuous action spaces, as opposed to discrete teleportation.
- Supports multiple environment splits (train, val, test) and room types (homes, offices, etc.).

## See also

- [[lookahead VLN model]] ⚠️ ⚠️
- [[VLN-CE challenge]] ⚠️ ⚠️ ⚠️
- [[Habitat Simulator]]
- [[Continuous Vision-Language Navigation]] ⚠️