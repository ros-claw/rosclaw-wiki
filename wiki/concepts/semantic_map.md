---
id: semantic_map
title: Semantic Map
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:20:58'
last_reinforced: '2026-04-30T01:20:58'
supersedes: []
sources:
- papers/2502.13451.pdf
source_type: arxiv_paper
---

# Semantic Map

A **Semantic Map** is a spatial representation that provides a top-down grid encoding semantic categories of objects and regions. It serves as a structured environment model for navigation and object-level understanding, bridging raw geometric mapping with higher-level scene semantics.

## Overview

Unlike traditional occupancy or costmap grids, a Semantic Map labels each cell (or region) with semantic categories — such as "floor", "wall", "table", "chair", "door", "path" — enabling an agent to reason about not just *where* it can go, but *what* is in that space. This representation forms the backbone for many embodied AI tasks, including:

- **Navigation**: Planning paths that respect semantic constraints (e.g., walk on floor, avoid fragile objects).
- **Object grounding**: Associating detected objects with persistent map locations.
- **Task planning**: Querying locations like "find a chair" or "go to the kitchen".

## Characteristics

| Property | Description |
|---|---|
| **Type** | Spatial representation |
| **Usage** | Top-down grid that encodes semantic categories of objects and regions |
| **Common formats** | 2D grid with categorical labels per cell; sometimes multi-layered (e.g., separate channels for object, region, affordance) |
| **Construction** | Often built by fusing geometric SLAM (e.g., Occupancy Grid ⚠️) with semantic segmentation from vision models |

## Capabilities

- Provides a spatial structure for **navigation** with semantic awareness
- Enables **object-level understanding** of the environment — knowing not just free space but functional zones and identity of landmarks

## Relationships

- **Used by**: Annotated Semantic Map (ASM) — the ASM extends this base concept by attaching additional annotations (e.g., affordances, task relevance flags) to the grid cells.
- **Depends on**: SLAM or Semantic Segmentation ⚠️ for map building.

## See Also

- Semantic Mapping ⚠️
- Spatial AI ⚠️
- Semantic Navigation ⚠️
- Environment Representation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Semantic Map` --related_to ⚠️--> `SLAM` _(wikilink)_
