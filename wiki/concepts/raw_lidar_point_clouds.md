---
id: raw_lidar_point_clouds
title: Raw LiDAR Point Clouds
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:13:54'
last_reinforced: '2026-04-30T04:13:54'
supersedes: []
sources:
- papers/2505.19214.pdf
source_type: arxiv_paper
---

# Raw LiDAR Point Clouds

**Type:** Concept ⚠️

Raw LiDAR point clouds refer to the unprocessed, three-dimensional spatial data collected by LiDAR sensors, consisting of individual measurement points with coordinates (x, y, z) and often intensity values. Unlike filtered or aggregated representations (e.g., elevation maps, occupancy grids), raw point clouds retain the full, high-resolution geometry of the environment.

## Capabilities

- **Direct input for end-to-end policy learning:** Raw point clouds can be fed directly into neural network policies, bypassing hand-crafted feature extraction and reducing information loss.
- **Bypasses intermediate representations like elevation maps:** This avoids computational overhead, quantization errors, and noise sensitivity associated with map-based preprocessing.

## Advantage

Raw LiDAR point clouds provide dense spatial information without the computational overhead and noise sensitivity of intermediate map representations. By preserving the native resolution of the sensor, they enable more accurate geometric reasoning and robust perception in dynamic or unstructured terrains.

## Relationships

- **Contrasts with:** Depth-Based Perception ⚠️ — while depth maps (e.g., from stereo cameras) are 2.5D projections, raw LiDAR point clouds provide full 3D structure without occlusion-based depth ambiguity.
- **Used by:** Omni-Perception — this architecture leverages raw point clouds as its primary sensory input for learning locomotion and navigation policies.

## Source

- Paper: *"2505.19214.pdf"* (arXiv)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Raw LiDAR Point Clouds` --related_to ⚠️--> `Omni-Perception` _(wikilink)_
