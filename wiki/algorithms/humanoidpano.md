---
id: humanoidpano
title: HumanoidPano
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:47:14'
last_reinforced: '2026-04-29T21:47:14'
supersedes: []
sources:
- papers/2503.09010.pdf
source_type: arxiv_paper
---

# HumanoidPano

## Overview

HumanoidPano is a hybrid cross-modal perception framework that synergistically integrates panoramic vision and LiDAR sensing for [[Humanoid Robot|humanoid robots]]. It leverages a [[Spherical Vision Transformer]] ⚠️ ⚠️ architecture to produce accurate [[BEV Segmentation Maps]] ⚠️ ⚠️ from 360-degree inputs, overcoming the limited field-of-view and self-occlusion challenges that plague conventional camera-LiDAR fusion on bipedal platforms.

## Parameters & Architecture

| Parameter | Value |
|-----------|-------|
| **Architecture** | Spherical Vision Transformer with SGC, SDA, AUG |
| **Input Modalities** | [[Panoramic Camera]] ⚠️ ⚠️ and [[LiDAR]] |
| **Output** | [[BEV Segmentation Maps]] ⚠️ ⚠️ |

The framework processes synchronized panoramic imagery and LiDAR point clouds through a transformer backbone designed for spherical geometry.

## Key Capabilities

- Enables seamless fusion of 360-degree visual context with LiDAR depth for robust perception
- Overcomes self-occlusion and limited FOV inherent in humanoid robotic platforms
- Generates accurate BEV segmentation maps essential for navigation and obstacle avoidance
- Achieves state-of-the-art performance on the [[360BEV-Matterport Benchmark]]

## Components

HumanoidPano is built from three specialized modules:

- **Spherical Geometry-aware Constraints (SGC)** – Enforces geometric consistency between panoramic image pixels and LiDAR points on the sphere, mitigating distortion artifacts typical of equirectangular projections.
- **Spatial Deformable Attention (SDA)** – A deformable attention mechanism that adaptively samples features in spherical space, focusing computational resources on visually salient regions.
- **Panoramic Augmentation (AUG)** – A data augmentation pipeline that applies spherical-aware transformations (e.g., rotations, flips) to both image and point cloud modalities, improving generalization under varied robot poses.

## Relationships

| Relation | Target |
|----------|--------|
| Uses | [[Panoramic Camera]] ⚠️ ⚠️, [[LiDAR]], [[Spherical Vision Transformer]] ⚠️ ⚠️ |
| Depends on | [[360BEV-Matterport Benchmark]] |
| Implements | Cross-modal fusion for [[Humanoid Robot]] navigation |

## Benchmark Performance

On the [[360BEV-Matterport Benchmark]], HumanoidPano outperforms prior methods (including [[Frustum-PointNet]] ⚠️, [[LSS]] ⚠️, and flat-transformer baselines) by a significant margin in terms of BEV mean IoU and pixel accuracy. The method demonstrates particular strength in handling partial occlusions and variable robot height, which are common failure modes for humanoid perception systems.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HumanoidPano` --[[implements]] ⚠️ ⚠️--> `Humanoid Robot`
- `HumanoidPano` --[[implements]] ⚠️ ⚠️--> `LiDAR`
- `HumanoidPano` --[[based_on]] ⚠️--> `360BEV-Matterport Benchmark`
