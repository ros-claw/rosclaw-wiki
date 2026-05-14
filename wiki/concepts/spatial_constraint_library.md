---
id: spatial_constraint_library
title: Spatial Constraint Library
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:40:39'
last_reinforced: '2026-04-30T00:40:39'
supersedes: []
sources:
- papers/2509.10454.pdf
source_type: arxiv_paper
---

# Spatial Constraint Library

## Description

A library of spatial constraints that covers all spatial relationship types used in VLN ⚠️ (Vision-Language Navigation) instructions. It is part of the GC-VLN framework and is used to map graph queries to constraints. The library is queried via **DAG queries** to retrieve predefined spatial constraints.

## Parameters

- **Content**: All types of spatial relationships mentioned in VLN instructions.
- **Usage**: Retrieved using DAG queries within the GC-VLN system.

## Capabilities

- Provides predefined constraints for spatial relationship types.

## Relationships

- **part_of**: GC-VLN — the Spatial Constraint Library is a component of the GC-VLN framework, enabling translation of natural language spatial relations into structured graph constraints.

## Dependencies

- **depends_on**: DAG queries ⚠️ — retrieval mechanism for constraint lookup.
- **depends_on**: Spatial Reasoning ⚠️ — foundational concept for defining spatial relationship types.

## Uses

- Used by GC-VLN agents to ground instructions into spatial constraints for navigation.

## Source

Based on the paper *"[2509.10454] GC-VLN: Generalizable Cross-Modal Spatial Reasoning for Vision-Language Navigation"* (arxiv).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Spatial Constraint Library` --related_to ⚠️--> `GC-VLN` _(wikilink)_
