---
id: real_time_visual_language_map
title: Real-time visual-language map
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:36:24'
last_reinforced: '2026-04-30T01:36:24'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

# Real-time Visual-Language Map

A **real-time visual-language map** (RTVLM) is an [[online map representation]] ⚠️ that associates each spatial location with both **visual features** and **language embeddings**. By fusing these modalities, the map enables a robot to reason about its environment through natural language queries and commands, bridging perception and symbolic grounding.

## Description

A map that associates each spatial location with both visual descriptors and language-aligned embeddings, allowing the robot to find locations described in natural language. This representation is continuously updated as the robot explores, enabling real-time semantic understanding of the environment without offline preprocessing.

## Parameters

- **Type**: [[Online map representation]] ⚠️
- **Components**:
  - Visual features (e.g., from a deep neural network)
  - Language embeddings (e.g., from a text encoder aligned with visual features)
  - Spatial coordinates (in the robot’s frame or global metric map)

## Capabilities

- Provides **real-time semantic understanding** of the surroundings.
- Supports **language grounding** — the robot can interpret abstract or task-specific phrases like “find the red chair near the door” or “go to the charging station.”

## Relationships

- **`built_by`** → [[Online visual-language mapper]] — constructs and updates the RTVLM from sensor data and language inputs.
- **`used_by`** → [[Language indexing-based localizer]] — queries the map to localize the robot in terms of semantically meaningful places.

## Related Concepts

- [[Embodied AI]]
- [[Visual-language navigation]] ⚠️
- [[Semantic mapping]] ⚠️
- [[Sim-to-real transfer]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Real-time visual-language map` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Real-time visual-language map` --[[related_to]] ⚠️ ⚠️--> `Online visual-language mapper` _(wikilink)_
