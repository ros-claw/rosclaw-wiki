---
id: spatial_scene_graph_ssg
title: Spatial Scene Graph (SSG)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:36:05'
last_reinforced: '2026-04-29T20:36:05'
supersedes: []
sources:
- papers/2601.06806.json
source_type: arxiv_paper
---

# Spatial Scene Graph (SSG)

A **Spatial Scene Graph (SSG)** is a structured representation that explicitly captures the global spatial structure and semantics of an explored environment. Unlike a standard Scene Graph ⚠️ ⚠️ which focuses on individual objects and their relationships within a single view, an SSG aggregates information across multiple observations to build a unified, topologically-aware map of the entire space. This enables a robot to reason about locations, object placements, and navigable paths in a single abstract form.

## Capabilities

- **Represents global spatial structure and semantics**: The SSG encodes both geometric (layout, connectivity) and semantic (object categories, functional zones) properties of the environment.
- **Enables efficient navigation in zero-shot VLN**: By providing a compact world model, the SSG allows agents to perform Zero-Shot Visual Language Navigation ⚠️ without task-specific training, using natural language instructions to query the graph and plan paths.

## Usage

The SSG is used by SpatialNav, which builds and queries the graph to drive navigation decisions. It acts as the central knowledge layer that bridges perception (object detection, depth estimation) and high-level planning (instruction following, path selection).

## Related Concepts

- Scene Graph ⚠️ ⚠️ (local per-view representation)
- Embodied AI
- Topological Mapping

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Spatial Scene Graph (SSG)` --applies_to ⚠️--> `SpatialNav`
