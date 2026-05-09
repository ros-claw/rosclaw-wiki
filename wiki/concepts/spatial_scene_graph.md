---
id: spatial_scene_graph
title: Spatial Scene Graph
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:36:06'
last_reinforced: '2026-04-29T20:36:06'
supersedes: []
sources:
- papers/2601.06806.pdf
source_type: arxiv_paper
---

## Spatial Scene Graph

A **Spatial Scene Graph (SSG)** is a graph representation that explicitly captures the global spatial structure and semantics of an explored environment. It organizes objects and regions along with their spatial and semantic relationships, serving as a persistent global memory for embodied navigation agents.

### Definition

In the context of embodied AI, a Spatial Scene Graph is a structured knowledge base that encodes the spatial layout and semantic content of an environment. It is constructed incrementally during exploration and allows agents to reason about remote object locations and plan efficient paths without relying on task-specific training data.

### Components

An SSG consists of:

- **Nodes**: Represent objects (e.g., chair, table) and regions (e.g., kitchen, living room).
- **Edges**: Represent spatial relations between nodes (e.g., "on top of", "next to", "inside").

These components together form a hierarchical and relational map of the environment.

### Capabilities

- **Encode spatial relationships** between objects, enabling agents to infer object affordances and relative positions.
- **Enable global reasoning** without task-specific training, making it suitable for zero-shot generalization.
- **Bridge local observations and global planning**, allowing agents to use current sensory input in the context of the entire explored space.

### Role in Zero-Shot Visual Language Navigation (VLN)

In the [[SpatialNav]] framework, the Spatial Scene Graph allows the agent to reason about remote object locations and plan efficient paths without learning from navigation data. It provides the global context needed for zero-shot navigation agents to interpret natural language instructions and navigate to novel objects in unfamiliar environments. By storing a compressed but semantically rich spatial model, the SSG decouples perception from planning and supports reusable navigation knowledge.

### Relationships

- **Used by**: [[SpatialNav]] – the SpatialNav agent relies on the SSG as its global memory for reasoning and planning.
- **Depends on**: [[Semantic Mapping]] ⚠️ – the SSG is typically built upon semantic segmentation and object detection outputs.
- **Part of**: [[Scene Understanding]] ⚠️ – the SSG is a key component for holistic spatial intelligence in embodied agents.

For further reading, see the source paper: *SpatialNav: A Zero-Shot Visual Language Navigation Framework* (arxiv: 2601.06806).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Spatial Scene Graph` --[[applies_to]] ⚠️--> `SpatialNav`
