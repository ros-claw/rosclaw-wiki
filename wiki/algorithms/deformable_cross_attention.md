---
id: deformable_cross_attention
title: Deformable Cross-Attention
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:52:29'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# Deformable Cross-Attention

Deformable Cross-Attention is an attention mechanism that efficiently incorporates semantic and structural features from observed images into 3D Gaussians. It uses deformable sampling to attend to relevant image features, enabling computationally efficient integration of visual information into 3D representations. The mechanism extends standard cross-attention by allowing attention to focus on a set of learned, deformable sampling points rather than attending over the entire image feature grid.

## Parameters

- **Query**: regional Gaussians  
- **Key / Value**: image features  

## Capabilities

- Efficiently incorporates semantic and structural features from observed images into 3D Gaussians, making it suitable for dense 3D scene understanding from limited views.  
- Efficiently incorporates local image features into 3D Gaussian refinement.

## Role in EmbodiedOcc

Within [[EmbodiedOcc]], deformable cross-attention is used to update regional Gaussians based on image features. It enables the model to selectively attend to relevant image regions and propagate visual semantics into the 3D Gaussian representation, facilitating fine-grained occupancy prediction from embodied observation. The query (regional Gaussians) attends to the keys/values (image features) via deformable sampling points.

## Relationships

- **Used by**: [[EmbodiedOcc]] – Deformable cross-attention is a core component of the EmbodiedOcc architecture for updating regional Gaussians based on image features.

### 自动链接关系  
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**  
- `Deformable Cross-Attention` --[[extends]] ⚠️--> `EmbodiedOcc`