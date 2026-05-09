---
id: scene_graphs
title: Scene Graphs
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T00:31:02'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.18592.pdf
- papers/2308.04758.pdf
source_type: arxiv_paper
---

## Scene Graphs (概念)

**Scene Graphs** are compact symbolic representations of an environment's structure. They encode objects, their attributes, and spatial relationships in a graph format, enabling high-level reasoning for embodied AI tasks.

### Definition
A scene graph is a graph-based representation where entities (objects, regions) are nodes and spatial or semantic relations are edges. It abstracts the visual world into a set of nodes and edges, bridging perception and symbolic reasoning.

### Overview
Scene graphs abstract the visual world into a set of nodes (entities) and edges (relations). In the context of [[Embodied AI]], scene graphs bridge perception and symbolic reasoning, allowing agents to perform tasks that require understanding of object placement, navigability, and interaction constraints. Their domain is typically indoor environments.

### Parameters
- **Type**: Compact symbolic scene graphs — each node corresponds to an object or region, and edges denote relationships such as "on top of", "next to", "inside", or "connected to".
- **Elements**: Nodes (objects/regions) and edges (relationships).
- **Domain**: Primarily indoor environments.
- **Integration**: With BEV (Bird’s-Eye View) representations in [[BSG (BEV Scene Graph)]] — the global scene map in BSG is a scene graph that stores and organizes local BEV representations according to topological relations.

### Capabilities
- **Represent environment structure symbolically**: Unlike raw pixel or depth maps, scene graphs capture the semantic layout of a space in a human-interpretable form.
- **Enable neurosymbolic reasoning**: By combining learned perception (neural) with explicit graph manipulation (symbolic), agents can plan, infer, and query environment state without exhaustive simulation.
- **Organize spatial and topological information**: Structures both local and global spatial knowledge.
- **Support global reasoning and decision making**: Facilitates high-level planning and goal inference.
- **Provide structured scene understanding**: Summarizes the environment in a form amenable to querying and inference.

### Role in BSG (BEV Scene Graph)
In the [[BSG (BEV Scene Graph)]] framework, the global scene map is implemented as a scene graph. This graph stores and organizes local BEV representations according to topological relations, allowing the agent to maintain a coherent, scalable map of the environment across multiple viewpoints. The scene graph’s nodes correspond to BEV patches or regions, and edges encode spatial adjacency and connectivity.

### Construction
Scene graphs are efficiently constructed during the exploration phase using a [[Vision-Language Models (VLM)]] ⚠️ ⚠️ based search. The VLM detects objects and their spatial relations from real-time sensor data, then builds or updates the graph incrementally. This approach avoids costly 3D reconstruction and remains robust to partial observability.

### Relationships
- **Used by**: [[VLN-Zero]] — a Vision-Language Navigation framework that relies on scene graphs for path planning and goal reasoning; [[BSG (BEV Scene Graph)]] — uses scene graphs as the global map layer.
- **Depends on**: [[Vision-Language Models (VLM)]] ⚠️ ⚠️ for object detection and relation extraction, and implicitly on [[ROS2]] or similar middleware for sensor data integration.
- **Related concepts**: [[Knowledge Graphs]] ⚠️ ⚠️, [[Semantic Mapping]] ⚠️ ⚠️, [[Symbolic Reasoning]] ⚠️ ⚠️, [[Neurosymbolic AI]] ⚠️ ⚠️, [[Spatial Memory]] ⚠️ ⚠️, [[Environment Representation]] ⚠️ ⚠️.

### See Also
- [[Knowledge Graphs]] ⚠️ ⚠️
- [[Semantic Mapping]] ⚠️ ⚠️
- [[Symbolic Reasoning]] ⚠️ ⚠️
- [[Neurosymbolic AI]] ⚠️ ⚠️
- [[Spatial Memory]] ⚠️ ⚠️
- [[Environment Representation]] ⚠️ ⚠️

---

*Sources: ArXiv paper 2509.18592 (Scene Graph Construction via VLM-based Exploration); ArXiv paper 2308.04758 (BSG: BEV Scene Graph for Embodied Navigation)*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Scene Graphs` --[[related_to]] ⚠️--> `Embodied AI`