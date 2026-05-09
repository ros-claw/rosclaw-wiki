---
id: lidar
title: LiDAR
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:41:24'
last_reinforced: '2026-04-29T21:41:24'
supersedes: []
sources:
- papers/2505.19214.pdf
source_type: arxiv_paper
---

# LiDAR

**LiDAR** (Light Detection and Ranging) is a 3D range sensor that serves as a primary sensing modality for [Omni-Perception]. It provides high-resolution point clouds of the surrounding environment, enabling robust spatial awareness across varied lighting conditions.

## Parameters

- **Type**: 3D range sensor
- **Role**: Primary sensing modality for [Omni-Perception]

## Capabilities

- Provides raw point clouds suitable for end-to-end learning
- Operates reliably in varied lighting conditions (day, night, indoor, outdoor)
- Enables 3D spatial awareness for navigation, obstacle detection, and scene understanding

## Relationships

- **Used by**: 
  - [Omni-Perception] — as its primary sensing channel
  - [PD-RiskNet] — for risk-aware planning in dynamic environments

LiDAR point clouds are typically processed through neural networks to extract geometric features, often in combination with other modalities (e.g., cameras, IMUs) for robust embodied perception.