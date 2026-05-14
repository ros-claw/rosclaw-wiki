---
id: matterport3d_dataset
title: Matterport3D Dataset
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-30T04:42:08'
last_reinforced: '2026-04-30T04:42:08'
supersedes: []
sources:
- code/peteanderson80_Matterport3DSimulator/README.md
source_type: official_manual
---

# Matterport3D Dataset

**Matterport3D** is a large-scale indoor RGB-D dataset containing densely sampled 360° panoramic imagery from real-world environments. It provides high visual complexity and serves as a core resource for embodied AI and navigation research.

## Parameters

| Parameter | Value |
|-----------|-------|
| Number of environments | 90 |
| Environment types | homes, offices, churches, hotels |
| Viewpoints per environment | 8–349 |
| Average spacing between viewpoints | 2.25 m |
| Available data types | matterport skybox images, undistorted depth images, undistorted camera parameters |

## Capabilities

- Provides densely sampled 360° indoor RGB-D images
- Real (not synthetic) visual data with high visual complexity
- Supports navigation research tasks (e.g., Visual Navigation, Embodied AI)

## Relationships

- Used by **Matterport3D Simulator** ‒ *uses*.
- Part of the **Matterport3D Simulator** project ‒ *part_of*.
- Often used in conjunction with ROS2 Navigation Stack ⚠️ for real-world sim-to-real transfer.

## Source

This page is derived from the official Matterport3D Simulator README (`data/raw/...`).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Matterport3D Dataset` --related_to ⚠️--> `Embodied AI`
- `Matterport3D Dataset` --depends_on ⚠️--> `Matterport3D Simulator`
