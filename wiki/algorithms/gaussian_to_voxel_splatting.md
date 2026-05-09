---
id: gaussian_to_voxel_splatting
title: Gaussian-to-voxel Splatting
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:52:50'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# Gaussian-to-voxel Splatting

**Gaussian-to-voxel Splatting** is a rendering algorithm that transforms 3D semantic Gaussians into a global 3D occupancy grid. It serves as the final output stage in the [[EmbodiedOcc]] pipeline, converting refined Gaussian splats into dense voxel occupancy predictions. This splatting technique projects 3D Gaussians onto a voxel grid to produce the final occupancy prediction.

## Parameters

- **Input**: 3D Gaussians with semantic features
- **Output**: voxelized occupancy grid

## Capabilities

- Renders 3D semantic Gaussians into a global 3D occupancy grid, enabling dense 3D scene understanding from Gaussian-based representations.
- Converts continuous Gaussian representation to discrete voxel occupancy.

## Function

Converts the refined 3D Gaussians to voxel occupancy for final output. This step bridges learned Gaussian primitives (which are continuous and unordered) with a discrete, grid-aligned occupancy representation suitable for downstream tasks such as navigation, manipulation, or planning.

## Relationships

- **used_by** → [[EmbodiedOcc]]  

  Gaussian-to-voxel Splatting is a core algorithm within the EmbodiedOcc system, which performs holistic 3D scene perception from RGB images. It depends on preceding stages that produce the semantic Gaussians, and implements the final occupancy decoding.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Gaussian-to-voxel Splatting` --[[extends]] ⚠️--> `EmbodiedOcc`