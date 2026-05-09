---
id: hierarchical_graph_representation
title: Hierarchical Graph Representation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:38:55'
last_reinforced: '2026-04-29T20:38:55'
supersedes: []
sources:
- papers/2403.09412.pdf
source_type: arxiv_paper
---

# Hierarchical Graph Representation

**Hierarchical Graph Representation** is a multi-level graph structure for representing large-scale outdoor environments, based on [[Lane Graph Connectivity]]. It serves as a core component of the [[OpenGraph]] system, enabling scalable semantic understanding and navigation.

## Description

The environment is segmented into regions using lane connectivity, then objects are attached to nodes, enabling hierarchical navigation and semantic understanding. This representation supports both query and navigation tasks across complex outdoors scenes.

## Parameters

- **Structure**: Multi-level graph based on lane graph connectivity.
- **Components**: Object nodes, lane segments, and their connections.

## Capabilities

- Scalable to large-scale outdoor environments.
- Supports query and navigation tasks.

## Relationships

- **Part of**: [[OpenGraph]]
- **Depends on**: [[Lane Graph Connectivity]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Hierarchical Graph Representation` --[[related_to]] ⚠️--> `OpenGraph` _(wikilink)_
