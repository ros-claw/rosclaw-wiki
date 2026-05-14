---
id: topological_map_navigation
title: Topological Map (navigation)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:21:24'
last_reinforced: '2026-04-30T01:21:24'
supersedes: []
sources:
- papers/2405.10620.pdf
source_type: arxiv_paper
---

## Topological Map (Navigation)

A **topological map** in the context of embodied navigation is a graph-based representation that encodes spatial knowledge as a set of **viewpoints** (e.g., distinct locations), **objects** observed at those viewpoints, and the **spatial relationships** between them. Rather than storing precise metric coordinates, a topological map captures the connectivity and salience of places, making it especially suitable for language-guided navigation and long-horizon tasks.

### Description

In the MC-GPT architecture, a topological map is used to store the agent's navigation experience. It retains:

- **Viewpoints** — key positions visited during exploration.
- **Objects** — detected or described objects associated with each viewpoint.
- **Spatial relationships** — how viewpoints and objects connect (e.g., "next to", "facing", "precedes").

This map also serves as the **global action space** for the agent, meaning the LLM ⚠️ ⚠️-based planner selects the next navigation action by choosing a node (viewpoint) from the map rather than regressing continuous coordinates. This simplifies decision-making and leverages the map's semantic structure.

### Role

The topological map enhances **memory construction** for long-term navigation tasks. By persisting a growing graph of visited places and their content, the agent can revisit past locations, recall object associations, and plan multi-step routes without traversing the environment anew. It is a core component that bridges short-term sensor observations with long-term episodic memory.

### Parameters

| Parameter | Description |
|-----------|-------------|
| **Stores** | viewpoints, objects, spatial relationships |
| **Serves as** | global action space for the planner |

### Capabilities

- Retains navigation history across episodes.
- Provides a structured, traversable action space for an LLM ⚠️ ⚠️-based agent, enabling reasoning over spatial sequences.

### Relationships

- **Part of**: MC-GPT — the topological map is a fundamental sub-component of the MC-GPT framework.
- **Used by**: Memory Map ⚠️ — the topological map's structure and data are consumed by a higher-level memory module for decision-making and recall.

### See Also

- SLAM — classical metric-based mapping (contrast with topological approach).
- Scene Graph ⚠️ — a richer semantic map that extends topological nodes with object attributes and relations.
- Embodied Navigation — broader context where topological maps are applied.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Topological Map (navigation)` --related_to ⚠️ ⚠️--> `MC-GPT` _(wikilink)_
- `Topological Map (navigation)` --related_to ⚠️ ⚠️--> `SLAM` _(wikilink)_
