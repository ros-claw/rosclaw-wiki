---
id: explicit_semantic_map
title: Explicit Semantic Map
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:51:38'
last_reinforced: '2026-04-30T02:51:38'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

## Explicit Semantic Map

An **Explicit Semantic Map** is a spatial representation built by the [[Grounded Semantic Mapping Network (GSMN)]] that stores learned information in a world reference frame. Unlike implicit or latent representations, this map provides an interpretable and geometrically consistent encoding of the environment, enabling the model to reason explicitly about spatial relationships between objects and locations.

### Capabilities

- **World‑reference storage** – Learned semantic information is maintained in a global coordinate frame, allowing the map to persist across viewpoints and agent movements.
- **Interpretable representation** – The structure of the map is human‑readable, making it possible to inspect what the model has learned about the environment.
- **Geometric consistency** – The map integrates a [[pinhole camera projection model]] to ensure that projected positions align correctly with observed images, preserving metric accuracy.

### Relationships

- **part_of** [[Grounded Semantic Mapping Network (GSMN)]]

The Explicit Semantic Map is a core component of the GSMN architecture. It is constructed from per‑image pixel‑wise semantic predictions and then fused into the global coordinate system using camera intrinsics and pose estimates. This map can be queried for downstream tasks such as [[semantic navigation]] ⚠️ or [[spatial reasoning]] ⚠️.

### See also

- [[Semantic Mapping]] ⚠️
- [[Scene Graph]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Explicit Semantic Map` --[[related_to]] ⚠️--> `Grounded Semantic Mapping Network (GSMN)` _(wikilink)_
