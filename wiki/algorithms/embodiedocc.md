---
id: embodiedocc
title: EmbodiedOcc
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:51:22'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# EmbodiedOcc

**EmbodiedOcc** is a Gaussian-based framework for **embodied 3D occupancy prediction** from monocular images. It enables a robot or agent to progressively build a full 3D occupancy map of its environment by exploring and integrating observations over time, using an explicit memory represented as 3D Semantic Gaussians ⚠️ ⚠️ ⚠️ ⚠️.

## Parameters

- **Input**: RGB images from an embodied agent
- **Output**: 3D occupancy grid
- **Internal Representation**: 3D Gaussians (semantic features, position, covariance, opacity)

## Overview

EmbodiedOcc initializes a global scene representation with uniformly distributed 3D semantic Gaussians. As the embodied agent moves and observes new regions, the model extracts features from each incoming RGB image and uses Deformable Cross-Attention to refine the Gaussians within that local region. After each refinement, Gaussian-to-voxel Splatting produces a global occupancy grid that integrates all past observations, enabling complete predictions even for occluded or unobserved parts of the scene.

## Capabilities

- Embodied 3D occupancy prediction from monocular images.
- Progressive scene understanding via embodied exploration.
- Maintains explicit global memory with 3D Semantic Gaussians ⚠️ ⚠️ ⚠️ ⚠️.
- Local refinement of regional Gaussians using Deformable Cross-Attention.
- Gaussian-to-voxel Splatting for occupancy output.

## Architecture

The pipeline consists of three main stages:

1. **Global Gaussian Initialization** – The entire scene volume is seeded with a uniform grid of 3D semantic Gaussians, each storing a feature vector representing occupancy and semantics.
2. **Local Refinement via Deformable Cross-Attention** – For each new monocular camera image, the model identifies the local region visible to the agent. Within that region, it uses deformable cross-attention to attend to image features and update the corresponding Gaussians’ parameters (position, covariance, opacity, semantic logits).
3. **Gaussian-to-Voxel Splatting** – To produce the final occupancy grid, the refined Gaussians are “splatted” into voxel space using a differentiable rendering-like operation. Each voxel accumulates contributions from overlapping Gaussians, yielding per-voxel occupancy and semantic probabilities.

## Relationships

| Relationship | Entity |
|--------------|--------|
| `uses` | 3D Semantic Gaussians ⚠️ ⚠️ ⚠️ ⚠️ (Gaussian representation) |
| `uses` | Deformable Cross-Attention |
| `uses` | Gaussian-to-voxel Splatting |
| `depends_on` | Embodied agent (e.g., robot with camera) |
| `depends_on` | Monocular camera images ⚠️ |
| `depends_on` | Embodied 3D Occupancy Prediction |

## Performance

EmbodiedOcc achieves state-of-the-art results on the **EmbodiedOcc-ScanNet** benchmark, a reorganized version of ScanNet designed for embodied occupancy evaluation. It outperforms prior methods by a significant margin in both geometric completeness and semantic accuracy, especially in scenes with large unobserved holes.

## Limitations

- Requires a predefined 3D volume extent for the global scene.
- Relies on high-quality depth priors or multiple viewpoints to resolve ambiguities; monocular depth estimation errors can affect the Gaussian refinement.
- The computational cost of deformable cross-attention scales with the number of Gaussians in the local region.

## References

- Paper: [arXiv 2412.04380](https://arxiv.org/abs/2412.04380)
- Related: Embodied 3D Occupancy Prediction, 3D Semantic Gaussians ⚠️ ⚠️ ⚠️ ⚠️, Occupancy Networks ⚠️