---
id: vision_centric_embodied_navigation_framework
title: Vision-Centric Embodied Navigation Framework
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:20:23'
last_reinforced: '2026-04-29T21:20:23'
supersedes: []
sources:
- papers/2602.06427.pdf
source_type: arxiv_paper
---

# Vision-Centric Embodied Navigation Framework

## Overview

The **Vision-Centric Embodied Navigation Framework** is an algorithm for instruction-driven embodied navigation that operates solely on image-based prompts and egocentric visual observations. It eliminates the need for precise coordinate systems or external maps, instead relying on a vision-centric policy to drive decision-making. The framework is particularly designed for **out-to-in navigation**—guiding an agent from an arbitrary starting location to a specified target location described via an image prompt.

## Key Features

- **Input Modality:** RGB images only  
- **Prompt Type:** Image-based prompts (target location represented as an image)  
- **Decision Driven By:** A vision-centric policy trained end-to-end  
- **Data Generation:** Uses trajectory-conditioned video synthesis to augment training data  

## Method

The framework processes an egocentric image of the agent’s current view alongside an image prompt of the target scene. A learned vision-based controller predicts the next action (e.g., movement, rotation) without requiring any explicit map or coordinate system.  

To handle the scarcity of real-world out-to-in navigation data, the authors introduce a **trajectory-conditioned video synthesis** pipeline. This data augmentation technique generates synthetic training episodes by conditioning video output on a target trajectory, enabling the policy to generalize to novel environments and start-target configurations.

## Capabilities

- Drives decision-making using image-based prompts (retrieved or captured images)  
- Integrates trajectory-conditioned video synthesis to generate large-scale training data for out-to-in navigation  
- Outperforms state-of-the-art baselines in both success rate and path efficiency on out-to-in navigation benchmarks  

## Relationships

- **Uses:**  
  - Image-Based Prompts ⚠️  
  - Trajectory-Conditioned Video Synthesis ⚠️  

- **Implements:**  
  - Out-to-In Prior-Free Instruction-Driven Embodied Navigation  

- **Part of:**  
  - Embodied Navigation (algorithm family)  

## Sources

- **Paper:** "Vision-Centric Embodied Navigation" (arXiv 2602.06427)

## Relevant Pages

- Embodied AI  
- Sim-to-Real Transfer  
- Egocentric Vision ⚠️  
- Navigation Policy ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Vision-Centric Embodied Navigation Framework` --based_on ⚠️ ⚠️--> `Out-to-In Prior-Free Instruction-Driven Embodied Navigation`
- `Vision-Centric Embodied Navigation Framework` --based_on ⚠️ ⚠️--> `Embodied AI`
