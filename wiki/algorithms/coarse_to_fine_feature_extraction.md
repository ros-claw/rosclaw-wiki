---
id: coarse_to_fine_feature_extraction
title: Coarse-to-Fine Feature Extraction
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:28:44'
last_reinforced: '2026-04-30T01:28:44'
supersedes: []
sources:
- papers/2403.14158.pdf
source_type: arxiv_paper
---

# Coarse-to-Fine Feature Extraction

**Coarse-to-Fine Feature Extraction** is a multi-scale feature extraction algorithm that processes a Volumetric Environment Representation (VER) by progressively refining details from coarse to fine granularity. It enables hierarchical scene understanding, allowing an embodied agent to first capture global spatial structure and then focus on local details relevant to navigation or manipulation tasks.

## Description

A multi-scale feature extraction approach that processes volumetric representation from coarse to fine granularity. The method operates on a volumetric grid (e.g., a dense 3D occupancy or feature grid) and applies a series of downsampling and upsampling operations, or uses a pyramid of resolutions, to extract features at each level. Coarse features capture high-level layout and landmarks, while fine features recover object boundaries, small obstacles, and surface details. The extracted multi-scale features are then fused or fed sequentially into downstream task heads.

## Capabilities

- Extracts features from VER at multiple resolutions.
- Enables hierarchical scene understanding by combining coarse layout cues with fine-grained geometric and semantic details.

## Relationships

- **Part of**: Volumetric Environment Representation, Multi-Task Learning for VLN
- **Depends on**: Volumetric Grid Representation ⚠️, hierarchical feature extraction techniques (e.g., U-Net, Feature Pyramid Networks)
- **Used by**: Vision-language navigation architectures that require both global and local context from 3D representations

## Integration

Within a multi-task learning framework, the coarse-to-fine features are shared across tasks such as goal prediction, obstacle avoidance, and path planning. The coarse branch typically output low-resolution feature maps for fast inference of long‑range dependencies, while the fine branch is activated only in regions of interest, reducing overall computational cost.