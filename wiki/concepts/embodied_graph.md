---
id: embodied_graph
title: Embodied Graph
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:56:01'
last_reinforced: '2026-04-29T23:56:01'
supersedes: []
sources:
- papers/2601.01872.pdf
source_type: arxiv_paper
---

# Embodied Graph

**Embodied Graph** is a multi-level semantic scene graph constructed using [[LLM]] ⚠️ ⚠️ ⚠️s that hierarchically integrates coarse-grained map data with fine-grained object entities within a temporal window. It serves as a retrievable knowledge base for [[RAG]] ⚠️ ⚠️ ⚠️ ⚠️ (Retrieval-Augmented Generation), enabling hierarchical semantic navigation and continuous adaptation to environmental changes. It is a core component of the [[CausalNav]] system.

## Architecture

The graph is structured across multiple levels:

- **Coarse-grained map data**: High-level spatial layout, room types, and topological connectivity.
- **Fine-grained object entities**: Individual objects, their properties, spatial relations, and interaction affordances.
- **Temporal window**: A continuous update mechanism that allows the graph to reflect changes in the environment over time.

The graph is constructed and updated by an [[LLM]] ⚠️ ⚠️ ⚠️ that processes observation sequences and outputs structured graph updates.

## Capabilities

- **Retrievable knowledge base for [[RAG]] ⚠️ ⚠️ ⚠️ ⚠️**: Embodied Graph stores environmental context that can be queried to ground downstream reasoning and decision-making.
- **Hierarchical semantic navigation**: Enables agents to plan at both coarse (room-level) and fine (object-level) granularities, supporting tasks like object search and goal-directed exploration.
- **Continuous update**: The graph evolves as the agent gathers new observations, maintaining an up-to-date representation of the dynamic environment.

## Relationships

| Type       | Target               | Description                                              |
|------------|----------------------|----------------------------------------------------------|
| `part_of`  | [[CausalNav]]        | Embodied Graph is a submodule of the CausalNav framework |
| `used_by`  | [[CausalNav]]        | CausalNav relies on the graph for scene understanding    |

## Details

The Embodied Graph is not a static map; it is designed for online construction and refinement. The LLM-based construction process takes raw observations (e.g., images, odometry) and outputs structured graph nodes and edges. The graph's temporal window mechanism ensures that outdated information can be pruned or revised, keeping the representation consistent with the current state of the world.

This structure directly supports the [[RAG]] ⚠️ ⚠️ ⚠️ ⚠️ paradigm: when an agent needs to answer a query about the environment, it retrieves relevant subgraphs from the Embodied Graph, rather than passing raw observations to the reasoning module.

## See Also

- [[Semantic Scene Graph]] ⚠️
- [[CausalNav]]
- [[LLM]] ⚠️ ⚠️ ⚠️
- [[RAG]] ⚠️ ⚠️ ⚠️ ⚠️
- [[Hierarchical Navigation]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Embodied Graph` --[[related_to]] ⚠️--> `CausalNav` _(wikilink)_
