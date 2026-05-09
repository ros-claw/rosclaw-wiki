---
id: semantickitti
title: SemanticKITTI
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T23:57:10'
last_reinforced: '2026-04-29T23:57:10'
supersedes: []
sources:
- papers/2403.09412.pdf
source_type: arxiv_paper
---

# SemanticKITTI

**SemanticKITTI** is a large-scale public dataset for autonomous driving and outdoor scene understanding. It provides dense semantic labels for LiDAR point clouds and corresponding camera images, serving as a primary benchmark for segmentation, mapping, and open-vocabulary understanding tasks.

## Overview

The dataset is derived from the [KITTI] odometry benchmark and offers full 360° semantic annotations for all sequences. It includes over 43,000 point cloud frames with 28 semantic classes (e.g., car, pedestrian, road, vegetation) and supports both *semantic segmentation* and *panoptic segmentation* tasks. SemanticKITTI is widely used to evaluate models in the [[Embodied AI]] community due to its challenging real-world variability in lighting, weather, and traffic conditions.

## Modalities

- **LiDAR point clouds**: High-resolution 3D scans captured with a Velodyne HDL-64E sensor.
- **Images**: Stereo camera images (left/right) synchronized with LiDAR frames.
- **Semantic labels**: Dense per-point annotations for 28 classes, plus instance IDs for panoptic benchmarks.

## Capabilities

- **Benchmarking**: Provides a standardized testbed for segmentation and mapping algorithms.
- **Open-vocabulary evaluation**: Supports assessment of models that map novel textual queries to point cloud regions, as demonstrated by [[OpenGraph]].

## Role in [[OpenGraph]]

SemanticKITTI is used for validation in the OpenGraph framework. OpenGraph achieved the highest segmentation and query accuracy on this dataset compared to prior methods, demonstrating robust open-vocabulary understanding in complex outdoor scenes.

## Relationships

- **Used by**: [[OpenGraph]] `uses` SemanticKITTI for validation.
- **Part of**: SemanticKITTI is a derivative of the [[KITTI]] ⚠️ ⚠️ dataset and is widely referenced alongside [[Waymo Open Dataset]] ⚠️ and [[nuScenes]] ⚠️ in the autonomous driving literature.
- **Depends on**: Utilizes [[LiDAR]] sensors and camera calibration conventions from the original [[KITTI]] ⚠️ ⚠️ setup.

## References

- Original paper: *SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences* (Behley et al., ICRA 2019).
- Source: `data/raw/papers/2403.09412.pdf` (discussed in context of [[OpenGraph]]).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SemanticKITTI` --[[related_to]] ⚠️--> `Embodied AI`
- `SemanticKITTI` --[[uses]] ⚠️--> `OpenGraph`
- `SemanticKITTI` --[[depends_on]] ⚠️--> `LiDAR`
