---
id: spatialnav
title: SpatialNav
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T20:35:57'
last_reinforced: '2026-04-29T20:35:57'
supersedes: []
sources:
- papers/2601.06806.json
source_type: arxiv_paper
---

# SpatialNav

SpatialNav is a zero-shot Vision-and-Language Navigation (VLN) ⚠️ agent that leverages a Spatial Scene Graph (SSG) to explicitly capture global spatial structure and semantics. It operates in the **Zero-shot VLN** domain, meaning it can navigate to goal locations specified in natural language without any task-specific training.

## Capabilities

- **Uses** Spatial Scene Graph (SSG) to explicitly encode the global spatial structure and semantic content of an environment.
- Integrates an **agent-centric spatial map** to guide navigation decisions.
- Employs a **compass-aligned visual representation** to maintain orientation consistency.
- Uses a **remote object localization strategy** to identify and remember locations of objects seen from a distance.
- Narrows the performance gap between zero-shot VLN agents and learning-based VLN methods.

## Dependencies

- **Depends on** the Zero-shot VLN setting — no explicit training on navigation tasks.
- **Depends on** access to an **explored environment** prior to task execution; it assumes the agent has already navigated through the environment to build an initial spatial graph.

## Relationships

- `uses`: Spatial Scene Graph (SSG)
- `depends_on`: Zero-shot VLN, explored environment (pre‑exploration)
- `improves_upon`: existing zero-shot VLN agents (e.g., previous heuristic or retrieval-based methods)

## Significance

SpatialNav demonstrates that explicit structured scene representations can dramatically improve the robustness of zero-shot VLN, achieving results competitive with fully-trained models without any finetuning. It highlights the importance of combining topological and semantic spatial knowledge for long-horizon navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SpatialNav` --related_to ⚠️--> `Spatial Scene Graph (SSG)`
