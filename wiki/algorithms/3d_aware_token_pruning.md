---
id: 3d_aware_token_pruning
title: 3D-Aware Token Pruning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:55:30'
last_reinforced: '2026-04-29T20:55:30'
supersedes: []
sources:
- papers/2507.05240.pdf
source_type: arxiv_paper
---

### 3D-Aware Token Pruning

**3D-Aware Token Pruning** is an algorithm for compressing historical visual states by leveraging the 3D spatial structure of visual data. It selectively prunes redundant tokens from a visual history, reducing memory footprint while preserving critical spatial information. This enables a bounded context size for processing long video streams, making it suitable for real-time or memory-constrained embodied AI systems.

#### Parameters

- **Awareness:** 3D spatial structure of the visual data
- **Purpose:** Compress historical visual states

#### Capabilities

- Reduces memory footprint of historical visual states
- Enables bounded context size for long video streams

#### Relationships

- **Used by:** [[StreamVLN]] uses 3D-Aware Token Pruning as part of its slow-updating memory context; also employed in [[SlowFast Context Modeling]].
- **Depends on:** the [[3D spatial structure of visual data]] ⚠️ to identify which tokens are spatially redundant and safe to prune.

The algorithm is described in the paper `papers/2507.05240.pdf` and forms a core component of the **StreamVLN** architecture, where it compresses historical frames within a slow-updating visual context buffer.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `3D-Aware Token Pruning` --[[extends]] ⚠️ ⚠️--> `StreamVLN`
- `3D-Aware Token Pruning` --[[extends]] ⚠️ ⚠️--> `SlowFast Context Modeling`
