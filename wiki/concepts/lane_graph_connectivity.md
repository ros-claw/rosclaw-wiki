---
id: lane_graph_connectivity
title: lane graph connectivity
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:00'
last_reinforced: '2026-04-29T23:58:00'
supersedes: []
sources:
- papers/2403.09412.pdf
source_type: arxiv_paper
---

## Lane Graph Connectivity

**Lane graph connectivity** is a representation of drivable lanes and their interconnections, used to partition the environment into hierarchically organized regions. It serves as a bridge between low-level perception (e.g., object detection) and high-level reasoning about drivable space.

### Parameters

- **Description**: Graph encoding the drivable lanes and their connectivity, enabling segmentation of the environment into hierarchical regions.

### Capabilities

- Enables **hierarchical segmentation** of outdoor scenes.
- Connects the **object-level map** to the **topological structure** of the environment.

### Relationships

- Used by [[OpenGraph]] to construct a navigable hierarchical representation of the scene.

### Role in OpenGraph

In the [[OpenGraph]] framework, the environment is segmented based on lane graph connectivity to construct a hierarchical graph. This structure aids in navigation, querying, and reasoning about spatial relationships at multiple levels of abstraction.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `lane graph connectivity` --[[related_to]] ⚠️--> `OpenGraph` _(wikilink)_
