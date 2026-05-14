---
id: hierarchical_scene_description_tree
title: Hierarchical Scene Description Tree
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:15:13'
last_reinforced: '2026-04-30T01:15:13'
supersedes: []
sources:
- papers/2502.11142.pdf
source_type: arxiv_paper
---

## Hierarchical Scene Description Tree

A **Hierarchical Scene Description Tree** is a tree-like representation that organizes 3D scene information from global layout to local details. It provides structured scene understanding and enables retrieval at different granularities, which is critical for generating context-aware instructions in embodied navigation tasks.

### Structure

The tree is built hierarchically, starting with the overall scene structure (e.g., room layout, floor plan) and progressively branching into finer details (e.g., furniture, objects, object parts). This allows both coarse-grained and fine-grained queries to be resolved efficiently.

### Capabilities

- **Structured 3D scene understanding** – Captures spatial and semantic relationships at multiple levels.
- **Granular retrieval** – Supports queries ranging from “what rooms are present?” to “where is the red cup on the kitchen table?”

### Construction and Usage

The tree is constructed automatically by a Large Language Model (LLM) ⚠️ ⚠️ that analyzes raw scene data (e.g., point clouds, CAD models, or natural language descriptions) and organizes them into a coherent hierarchy.

It is used by NavRAG to generate detailed navigation instructions by retrieving relevant scene context at the appropriate level of detail.

### Relationship Annotations

- **built_by** → Large Language Model (LLM) ⚠️ ⚠️  
- **used_by** → NavRAG  
- **depends_on** → Scene Graph ⚠️, 3D Object Detection ⚠️  

### Example

For a typical indoor environment:

```
Scene (House)
├── Floor 1
│   ├── Living Room
│   │   ├── Couch (blue sectional)
│   │   ├── Coffee Table (wooden, with magazines)
│   │   └── TV Stand
│   ├── Kitchen
│   │   ├── Countertop
│   │   ├── Refrigerator
│   │   └── Dining Table (with 4 chairs)
│   └── Hallway
├── Floor 2
│   ├── Bedroom 1
│   │   └── Bed (queen, with nightstands)
│   └── Bathroom
└── Garage
```

This tree allows NavRAG to answer queries like “go to the blue couch” by retrieving the exact node, or “describe the layout of the first floor” by summarizing the relevant sub-branch.

### Sources

- arXiv paper 2502.11142: *NavRAG: Generating User-Centered Instructions for Embodied Navigation via Retrieval-Augmented Generation*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Hierarchical Scene Description Tree` --related_to ⚠️--> `NavRAG` _(wikilink)_
