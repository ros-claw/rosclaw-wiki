---
id: explorfm
title: ExploRFM
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:34:33'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2602.19308.json
- articles/wildos.md
source_type: arxiv_paper
---

# ExploRFM

**ExploRFM** is a vision‑language foundation model designed for onboard semantic navigation tasks in autonomous robots. It integrates with the WildOS system to enable real‑time traversability prediction, visual frontier detection, and open‑vocabulary object similarity scoring over a long‑range visual horizon.

## Parameters

- **Type**: Vision‑language foundation model  
- **Inputs**: Image (from robot camera) and a text query  
- **Outputs**: 
  - Visual traversability  
  - Visual frontiers  
  - Open‑vocabulary object similarity  

## Capabilities

- Simultaneously predicts traversability, visual frontiers, and object similarity in image space.
- Operates over a **long‑range visual horizon** that extends beyond the reach of typical depth sensors.
- Enables real‑time onboard scoring of frontier nodes in a sparse navigation graph, based on semantic relevance to an open‑vocabulary user query.
- Confidence maps are thresholded and used to weight each frontier node.

## Relationships

- **Part of**: WildOS  
- **Uses**: Vision Foundation Models ⚠️ (a class of Foundation model ⚠️)  
- **Implements**: Traversability prediction ⚠️, Visual frontier detection ⚠️, Object similarity scoring ⚠️  

> **🔄 Discrepancy note**: The automated linker previously recorded an `extends` relationship from ExploRFM to WildOS. The source data confirms the relationship is `part_of`. Both are valid in different granularities – ExploRFM is a component *part of* WildOS, and its design also *extends* the capabilities of WildOS.

## Function

ExploRFM processes the current camera image together with an open‑vocabulary text query. It produces three prediction maps over the image: visual traversability, visual frontiers, and object similarity. These maps are combined and thresholded to generate scores for each frontier node in the navigation graph. The result is a real‑time, semantics‑aware navigation signal that allows the robot to explore toward user‑specified objects or terrain types.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**  
- `ExploRFM` --extends ⚠️--> `WildOS`  

*Note: see discrepancy note above.*