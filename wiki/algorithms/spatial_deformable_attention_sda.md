---
id: spatial_deformable_attention_sda
title: Spatial Deformable Attention (SDA)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:50:39'
last_reinforced: '2026-04-29T21:50:39'
supersedes: []
sources:
- papers/2503.09010.pdf
source_type: arxiv_paper
---

# Spatial Deformable Attention (SDA)

**Spatial Deformable Attention (SDA)** is a novel attention mechanism introduced in the context of the [[HumanoidPano]] framework. It is designed to efficiently aggregate hierarchical 3D features by leveraging spherical offsets, enabling geometrically complete object representations for 360°-to-BEV (Bird's Eye View) fusion.

## Overview

Traditional attention mechanisms struggle with the irregular sampling required for full spherical perception. SDA addresses this by learning deformable attention patterns in 3D space, parameterized as spherical offsets from reference points. This allows the model to focus on relevant 3D regions without the computational overhead of dense volumetric attention.

## Capabilities

- **Aggregates hierarchical 3D features via spherical offsets** – SDA adaptively selects multi-scale features from spherical or panoramic inputs, constructing a rich 360° representation.
- **Enables efficient 360°-to-BEV fusion with geometrically complete object representations** – By fusing panoramic views into a Bird’s Eye View, SDA produces output features that preserve the full geometry of objects, crucial for downstream embodied tasks such as navigation and manipulation.

## Relationships

- **Part of** [[HumanoidPano]] – SDA is a core component of the HumanoidPano architecture, which integrates panoramic perception and BEV representation for humanoid robotics.
- **Depends on** deformable attention primitives (e.g., [[Deformable Attention]] ⚠️ in transformers) extended to 3D spherical coordinates.
- **Used by** [[HumanoidPano]]’s feature extraction and fusion pipeline.

## References

- Source paper: [arxiv 2503.09010](https://arxiv.org/abs/2503.09010) – *HumanoidPano: Embodied Perception with 360° Panoptic Representation*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Spatial Deformable Attention (SDA)` --[[extends]] ⚠️--> `HumanoidPano`
