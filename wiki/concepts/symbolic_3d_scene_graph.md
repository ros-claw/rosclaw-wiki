---
id: symbolic_3d_scene_graph
title: symbolic 3D scene graph
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:23:59'
last_reinforced: '2026-04-30T00:23:59'
supersedes: []
sources:
- papers/2502.00931.pdf
source_type: arxiv_paper
---

# Symbolic 3D Scene Graph

A **Symbolic 3D Scene Graph** is a structured representation of a three-dimensional environment that encodes objects, their spatial relationships, and semantic attributes in a symbolic (non-raw) form. It serves as an intermediate abstraction that bridges low‑level geometric data (e.g., point clouds, meshes) with high‑level reasoning, particularly for Vision-Language Models (VLMs) ⚠️ and downstream robotic tasks.

## Description

A symbolic representation of the 3D environment used to enhance neural reasoning in VLM-based navigation. By converting dense geometric information into a compact, symbolic graph — where nodes represent objects or regions and edges encode relationships (e.g., “on top of”, “next to”, “inside”) — the scene graph enables more efficient and interpretable reasoning than raw sensor inputs. This representation is commonly built from SLAM output or reconstructed meshes and is designed to be consumed by symbolic or neuro‑symbolic planners.

## Capabilities

- Provide symbolic representation of environment – abstracts raw geometry into a queryable graph of entities and relations.
- Enhance VLM reasoning – supplies a well‑structured input that reduces the burden on learned vision‑language models to interpret cluttered 3D data.

## Relationships

- **Used by**:
  - NeSy Task Planner – neuro‑symbolic planner that reasons over the graph to generate action sequences.
  - VL-Nav – vision‑language navigation system that queries the scene graph for semantic cues.

## See Also

- Neuro-Symbolic Reasoning
- Semantic Mapping ⚠️
- 3D Scene Understanding ⚠️
- Graph Neural Networks (GNNs) ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `symbolic 3D scene graph` --related_to ⚠️--> `SLAM` _(wikilink)_
