---
id: 2d_3d_sampling
title: 2D-3D Sampling
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:25:42'
last_reinforced: '2026-04-30T01:25:42'
supersedes: []
sources:
- papers/2403.14158.pdf
source_type: arxiv_paper
---

## 2D-3D Sampling

**2D-3D Sampling** is an algorithm that maps 2D features extracted from multiple perspective views into a 3D voxel grid, enabling volumetric representation. It bridges the gap between 2D vision cues and 3D spatial understanding, forming a critical component in embodied perception pipelines.

### Description

2D-3D Sampling aggregates multi-view 2D features into unified 3D volumetric cells. By projecting 2D feature maps onto a voxel grid according to camera geometry, each voxel accumulates contributions from all views where it is visible. The resulting 3D volume retains both geometric shape and semantic information, supporting downstream tasks such as navigation, manipulation, and scene understanding.

### Capabilities

- Aggregates multi-view 2D features into unified 3D volumetric cells.

### Relationships

- **uses** – 2D feature extraction ⚠️ to obtain per-view descriptors.
- **part_of** – Volumetric Environment Representation, a broader paradigm for encoding spatial knowledge in embodied agents.