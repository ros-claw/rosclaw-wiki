---
id: dual_implicit_neural_memory
title: Dual Implicit Neural Memory
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:30:17'
last_reinforced: '2026-04-30T00:30:17'
supersedes: []
sources:
- papers/2509.22548.pdf
source_type: arxiv_paper
---

# Dual Implicit Neural Memory

**Dual Implicit Neural Memory** is a compact fixed-size neural representation paradigm for Vision-and-Language Navigation (VLN). It stores historical key-value caches from both spatial-geometric and visual-semantic encoders, retaining only tokens in initial and sliding window to enable efficient incremental updates and avoid redundant computation.

## Description

This novel approach models spatial-geometric and visual-semantic memory separately, allowing the agent to maintain a persistent, updatable memory that captures both the geometry of the environment and the semantics of visual language. By using implicit neural representations with sliding windows, the memory avoids unbounded growth while preserving critical information.

## Components

Dual Implicit Neural Memory consists of two specialized memory modules:

- **[[Spatial-Geometric Memory]] ⚠️**: Represents 3D spatial layout and geometric properties of the environment, enabling the agent to reason about positions, distances, and physical constraints.
- **[[Visual-Semantic Memory]] ⚠️**: Encodes high‐level semantic features of images and language grounding, allowing the agent to remember visually relevant objects, scenes, and linguistic cues.

Both are implemented as compact fixed‐size key‐value caches that are incrementally updated as the agent navigates.

## Capabilities

- Models spatial-geometric and visual-semantic memory separately for more effective representation.
- Enables efficient incremental updates without reprocessing the entire history.
- Avoids redundant computation by discarding old tokens outside the sliding window.
- Supports long‐horizon navigation tasks by retaining only the most relevant information.

## Relationships

| Relation | Entity | Description |
|----------|--------|-------------|
| `used_by` | [[JanusVLN]] | Dual Implicit Neural Memory is employed as the memory module in the JanusVLN framework. |
| `depends_on` | [[Spatial-Geometric Encoder]] ⚠️ | Relies on a spatial-geometric encoder to produce the geometric feature cache. |
| `depends_on` | [[Visual-Semantic Encoder]] ⚠️ | Uses a visual-semantic encoder to generate the semantic feature cache. |

This approach is designed to be agnostic to the specific encoder implementations, making it a general memory architecture for embodied navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Dual Implicit Neural Memory` --[[related_to]] ⚠️--> `JanusVLN` _(wikilink)_
