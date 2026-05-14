---
id: hierarchical_multi_modal_scene_graph
title: Hierarchical Multi-modal Scene Graph
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:52:20'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.13733.pdf
source_type: arxiv_paper
---

# Hierarchical Multi-modal Scene Graph

**HMSG** (Hierarchical Multi-modal Scene Graph) is a multi-modal map representation algorithm designed to support progressive retrieval — moving from coarse room-level understanding down to fine-grained goal views and object identification. It provides a unified representation that integrates diverse sensory modalities, enabling efficient hierarchical querying from high-level room information to precise goal view and object-level details. HMSG is primarily used by the FSR-VLN navigation framework.

## Description

HMSG provides a multi-modal map representation supporting progressive retrieval, from coarse room-level localization to fine-grained goal view and object identification. This hierarchical structure allows agents to first localize at the room level, then refine through goal views, and finally identify specific objects, matching the typical reasoning flow of visual-language navigation tasks.

## Parameters

The algorithm itself is parameterized by its hierarchical structure rather than explicit numeric parameters. The type is defined as a hierarchical multi-modal scene graph.

## Capabilities

- Multi-modal map representation that integrates diverse sensory modalities (visual, linguistic, spatial).
- Progressive retrieval: enables hierarchical querying from coarse room-level localization to fine-grained goal views and object identification.

## Relationships

- **used_by**: FSR-VLN — HMSG provides the map representation and retrieval pipeline for this visual language navigation system.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Hierarchical Multi-modal Scene Graph` --extends ⚠️--> `FSR-VLN`