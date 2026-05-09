---
id: data_domain_gap
title: Data Domain Gap
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:44:25'
last_reinforced: '2026-04-29T20:44:25'
supersedes: []
sources:
- papers/2512.15258.json
source_type: arxiv_paper
---

# Data Domain Gap

A **Data Domain Gap** refers to the distributional mismatch between the data used to train a machine learning model (e.g., simulation, synthetic, or offline datasets) and the real-world data encountered during deployment. This gap often leads to performance degradation, particularly in vision-language-action (VLA) models for robotics.

## Problem for Aerial Navigation VLA Models

The Data Domain Gap is a critical challenge for [[VLA Models]] ⚠️ ⚠️ applied to [[Aerial Navigation]] ⚠️ ⚠️. Aerial platforms operate in highly dynamic environments with diverse lighting, textures, weather, and obstacle types, making it difficult for models trained on limited or synthetic data to generalize effectively. Specific issues include:

- Lack of photorealism in synthetic training data
- Missing edge cases or rare sensor noise patterns
- Differences in camera intrinsics and motion blur between sim and real

## Mitigation via High-Fidelity Datasets using 3D-GS

A promising approach to reducing the Data Domain Gap is constructing **high-fidelity datasets using [[3D Gaussian Splatting (3D-GS)]]** (addressed by paper [[2512.15258]] ⚠️). 3D-GS enables the generation of photorealistic, novel-view synthetic images from a sparse set of real captures, bridging the visual fidelity gap. This method:

- Preserves fine-grained textures and lighting details
- Allows dense coverage of viewpoints without exhaustive real-world data collection
- Produces consistent, physically plausible sensor inputs for training

By using such a dataset, aerial navigation VLA models can be pre-trained or fine-tuned on data that more closely matches the deployment domain, thereby increasing robustness.

## Relationship Annotations

- **depends_on**: [[3D Gaussian Splatting]], [[High-Fidelity Dataset Generation]] ⚠️, [[Domain Adaptation]] ⚠️
- **problem_for**: [[Aerial Navigation]] ⚠️ ⚠️, [[VLA Models]] ⚠️ ⚠️
- **mitigated_by**: [[3D-GS-based Dataset Augmentation]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Data Domain Gap` --[[related_to]] ⚠️ ⚠️--> `3D Gaussian Splatting (3D-GS)` _(wikilink)_
- `Data Domain Gap` --[[related_to]] ⚠️ ⚠️--> `3D Gaussian Splatting` _(wikilink)_
