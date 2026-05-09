---
id: spatialnav
title: SpatialNav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:35:56'
last_reinforced: '2026-04-29T20:35:56'
supersedes: []
sources:
- papers/2601.06806.pdf
source_type: arxiv_paper
---

# SpatialNav

SpatialNav is a zero-shot [[vision-and-language navigation]] (VLN) agent that leverages [[Spatial Scene Graph]] (SSG) to capture global spatial structure and semantics from explored environments. It integrates an agent-centric spatial map, compass-aligned visual representation, and remote object localization strategy for efficient navigation without task-specific training.

## Overview

SpatialNav is a zero-shot VLN agent that exploits [[Spatial Scene Graph]] to explicitly capture global spatial structure and semantics from explored environments. It enables efficient exploration and navigation in both discrete and continuous environments by integrating three key components: an agent-centric spatial map, a compass-aligned visual representation, and a remote object localization strategy. The agent requires no task-specific fine‑tuning, relying entirely on the structured spatial knowledge encoded in the scene graph.

## Architecture

The agent constructs a [[Spatial Scene Graph]] from exploration, then uses it for global planning. Key components include:

- **Agent-centric spatial map** – encodes local observations from the robot’s perspective into a compact metric representation.
- **Compass-aligned visual representation** – aligns visual features with a global compass frame to maintain orientation consistency across the graph.
- **Remote object localization module** – locates distant targets by reasoning over the spatial relationships in the scene graph, enabling goal‑directed navigation without prior exposure.

## Capabilities

- Zero-shot vision-and-language navigation – understands natural language instructions without task‑specific training.
- Explicit global spatial structure exploitation – uses the [[Spatial Scene Graph]] to reason about room layouts and object placements.
- Efficient exploration and navigation in discrete and continuous environments – adapts to both simulated grids and real‑world continuous spaces.

## Relationships

- **Uses** → [[Spatial Scene Graph]]
- **Depends on** → [[Spatial Scene Graph]]
- **Related to** → [[zero-shot learning]], [[embodied navigation]], [[scene understanding]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SpatialNav` --[[based_on]] ⚠️ ⚠️--> `vision-and-language navigation`
- `SpatialNav` --[[based_on]] ⚠️ ⚠️--> `Spatial Scene Graph`
