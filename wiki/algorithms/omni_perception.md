---
id: omni_perception
title: Omni-Perception
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:38:52'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.19214.pdf
source_type: arxiv_paper
---

---

# Omni-Perception

**Type:** Algorithm (End-to-end locomotion policy)  
**Confidence:** 0.85 (reinforced by source: `papers/2505.19214.pdf`)

## Overview

Omni-Perception is an end-to-end locomotion policy for legged robots that directly processes raw LiDAR point clouds to produce motor commands. Unlike traditional approaches that rely on intermediate elevation maps or occupancy grids, Omni-Perception maintains full 3D spatial awareness and achieves omnidirectional collision avoidance in dynamic environments. It is designed to be robust to sensor noise, lighting variability, aerial clutter, uneven terrain, and the presence of other dynamic agents.

| Parameter | Value |
|-----------|-------|
| Sensing input | Raw LiDAR point clouds |
| Spatial awareness | 3D |
| Avoidance type | Omnidirectional in dynamic environments |

The policy integrates the PD-RiskNet perception module for spatio-temporal risk assessment, enabling direct end-to-end learning from raw sensor data without intermediate map representations.

## Methodology

Omni-Perception directly processes raw LiDAR point clouds through PD-RiskNet to produce reactive control policies for legged locomotion, avoiding any intermediate map representations. This end-to-end approach allows the policy to leverage the full density and spatial detail of point cloud data, improving robustness under real-world conditions where map-based methods often fail.

### Training

Training is performed using a high-fidelity LiDAR simulation toolkit that provides realistic noise modeling and fast raycasting. The policy has been validated across multiple simulation platforms:

- Isaac Gym ⚠️
- Genesis ⚠️
- MuJoCo ⚠️

This diverse training environment supports effective sim-to-real transfer by exposing the policy to varied sensor noise profiles and dynamics.

## Capabilities

- 3D spatial awareness without elevation maps
- Omnidirectional collision avoidance in dynamic 3D environments
- Robust to sensor noise and lighting variability
- Handles aerial clutter, uneven terrain, and dynamic agents
- Effective sim-to-real transfer using realistic LiDAR simulation
- End-to-end learning from raw LiDAR data

## Relationships

- **uses:** LiDAR sensor, PD-RiskNet
- **depends_on:** PD-RiskNet, high-fidelity LiDAR simulation toolkit
- **implements:** omnidirectional collision avoidance

## Application

Omni-Perception is designed for legged robot ⚠️ platforms that require robust, real-time navigation through unstructured and dynamic environments. It is particularly suited for tasks where traditional mapping pipelines introduce latency or fail due to sensor degradation.

## Related Pages

- PD-RiskNet
- LiDAR
- Sim-to-Real Transfer
- Legged Locomotion ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Omni-Perception` --extends ⚠️--> `PD-RiskNet`

---