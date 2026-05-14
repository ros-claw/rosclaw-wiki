---
id: open_vocabulary_map_outdoor
title: Open-Vocabulary Map (Outdoor)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:39:25'
last_reinforced: '2026-04-29T20:39:25'
supersedes: []
sources:
- papers/2403.09412.json
source_type: arxiv_paper
---

## Open-Vocabulary Map (Outdoor)

### Overview

Open-vocabulary maps extend traditional semantic mapping by supporting arbitrary, open-set classes defined through natural language, rather than a fixed taxonomy. While earlier work focused on small-scale indoor environments, the **Open-Vocabulary Map (Outdoor)** concept, as instantiated by OpenGraph and related methods, addresses the unique challenges of large-scale outdoor robotics. These maps combine Visual-Language Models (VLMs) with hierarchical 3D representations and **lane graph connectivity** to enable robust navigation and manipulation in unstructured outdoor settings.

### Characteristics

- **Open-vocabulary**: Supports zero-shot recognition of any class described in natural language, without requiring retraining on new categories.
- **Hierarchical**: Organizes spatial knowledge into multiple levels of abstraction (e.g., traversable lanes, semantic regions, objects).
- **3D**: Represents geometry and semantics in three dimensions, accommodating terrain and elevation changes.
- **Large-scale outdoor**: Optimized for environments such as roads, parks, and construction sites, where map size and dynamic elements are significant.

### Capabilities

- **Zero-shot and open-set class support**: Enables robots to interpret and act upon user commands like "go to the red fire hydrant" without prior examples of that specific object.
- **Outdoor navigation and manipulation**: Provides the semantic grounding needed for path planning along lanes, obstacle avoidance, and interaction with objects in open spaces.

### Limitations of Existing Approaches

Existing open-vocabulary maps were primarily designed for small-scale indoor scenes (e.g., rooms, corridors). They exhibit:
- **Limited understanding**: Inability to handle ambiguous or unstructured outdoor semantics (e.g., "parking lot" vs. "driveway").
- **Poor map structure**: Lack of hierarchical representations needed for lane-level navigation and large-area coverage.

Open-vocabulary maps (Outdoor) overcome these by integrating 3D mapping techniques ⚠️ ⚠️ ⚠️ with hierarchical lane graphs and VLM-derived descriptors.

### Dependencies

This concept **depends_on**:
- Visual-Language Models (VLMs) – for grounding natural language in visual features.
- 3D mapping techniques ⚠️ ⚠️ ⚠️ – for building and maintaining large-scale point clouds or voxel grids.
- **Lane graph connectivity** – for topological reasoning over drivable paths.

### Related Algorithms

The primary algorithm implementing this concept is OpenGraph, which performs graph-based open-vocabulary mapping and localization for outdoor robots.

### Relationship Annotations

- OpenGraph **implements** Open-Vocabulary Map (Outdoor)
- Open-Vocabulary Map (Outdoor) **depends_on** Visual-Language Models (VLMs)
- Open-Vocabulary Map (Outdoor) **depends_on** 3D mapping techniques ⚠️ ⚠️ ⚠️
- Open-Vocabulary Map (Outdoor) **depends_on** Lane graph connectivity

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Open-Vocabulary Map (Outdoor)` --related_to ⚠️ ⚠️--> `OpenGraph` _(wikilink)_
- `Open-Vocabulary Map (Outdoor)` --related_to ⚠️ ⚠️--> `Visual-Language Models (VLMs)` _(wikilink)_
