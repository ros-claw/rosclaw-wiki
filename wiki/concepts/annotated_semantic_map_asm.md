---
id: annotated_semantic_map_asm
title: Annotated Semantic Map (ASM)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:44:07'
last_reinforced: '2026-04-30T00:44:07'
supersedes: []
sources:
- papers/2502.13451.pdf
source_type: arxiv_paper
---

## Annotated Semantic Map (ASM)

### Definition

An **Annotated Semantic Map (ASM)** is a memory representation that transforms abstract semantic information into explicit navigable cues. Constructed as a top-down semantic grid, the ASM is populated with textual labels for key regions, precise object mappings, and structured navigation information. This representation is built at the start of an episode and updated each timestep, replacing traditional historical frame sequences to reduce memory and computational overhead while providing clear navigation directives derived from high-level semantics.

### Parameters

| Parameter | Description |
|-----------|-------------|
| **Type** | Memory representation |
| **Construction** | Top-down semantic map, initialized at episode onset, updated every timestep |
| **Features** | Explicit textual labels for key regions, precise object mapping, structured navigation information |
| **Source** | Derived from the [[MapNav]] framework (arxiv:2502.13451) |

### Capabilities

- Provides clear navigation cues from abstract semantics, enabling the agent to interpret high-level instructions directly from the map.
- Replaces historical frame sequences, significantly reducing memory footprint and computation compared to dense frame-based approaches.

### Relationships

- **Used by** → [[MapNav]]: The ASM serves as the core memory representation within the MapNav model.
- **Part of** → [[MapNav]] model: The ASM is an integral component of the MapNav architecture, enabling it to perform semantic navigation without relying on historical visual frames.

### See Also

- [[Semantic Map]]
- [[Top-Down Grid Representation]] ⚠️
- [[MapNav]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Annotated Semantic Map (ASM)` --[[related_to]] ⚠️--> `MapNav` _(wikilink)_
