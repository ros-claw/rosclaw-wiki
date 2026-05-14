---
id: retrieval_augmented_generation_rag
title: Retrieval-Augmented Generation (RAG)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T23:56:29'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2601.01872.pdf
- papers/2502.11142.pdf
source_type: arxiv_paper
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation** (RAG) is a technique that augments the output of a generative language model by first retrieving relevant information from an external knowledge base or structured memory. In embodied AI, RAG enables agents to answer open-vocabulary queries and generate context-aware plans by grounding generation in an explicit representation of the environment. This page documents RAG as used in the contexts of *CausalNav* (arXiv:2601.01872) and *NavRAG* (arXiv:2502.11142).

## Description  

RAG follows a pattern where an LLM retrieves external knowledge — here, scene descriptions — before generation to improve relevance and accuracy. The retrieval corpus is typically a structured representation of the environment, such as a graph or hierarchical tree.

## Capabilities

- **Enhances semantic navigation** by querying the Embodied Graph – the graph serves as the retrieval corpus, providing spatial and semantic facts about the environment.
- **Enables open-vocabulary query handling** – because retrieval is decoupled from generation, the system can respond to arbitrary natural language queries without re‑training.
- **Retrieves relevant scene information from a hierarchical tree** – in implementations like NavRAG, the retrieval structure is a tree encoding object‑scene relationships.
- **Supports diverse instruction generation** – the retrieved context can be fed to an LLM to produce different types of instructions (e.g., navigation, manipulation) from a single environment model.

## Parameters / Context Type

The type of context retrieved varies by implementation:
- In CausalNav, the retrieval corpus is the Embodied Graph — a graph of objects, locations, and causal relations.
- In NavRAG, the retrieval corpus is a hierarchical tree of 3D scene descriptions.

Both serve the same core purpose: grounding language generation in explicit world knowledge.

## Dependencies

- **depends_on** (general): An external knowledge structure (graph, tree, etc.) that encodes environmental facts.
- **depends_on** in CausalNav: Embodied Graph – the retrieved knowledge is drawn from this structured, updatable graph.
- **depends_on** in NavRAG: A hierarchical scene tree that organizes objects and spatial relations.

## Usage

- **used_by**: CausalNav – CausalNav employs RAG to fetch relevant subgraphs or node descriptions from the Embodied Graph, which are then fed to a planner or language model to generate step‑by‑step navigation instructions.
- **used_by**: NavRAG – NavRAG uses RAG to retrieve relevant scene‑tree nodes before generating diverse navigation or manipulation instructions.
- **part_of**: NavRAG framework ⚠️ – RAG is a core component of the NavRAG architecture.

## Role in CausalNav

In the CausalNav system, RAG is used to retrieve relevant spatial and semantic information from the Embodied Graph in order to generate navigation plans in response to language queries. The retrieval step selects nodes and edges that are most relevant to the query (e.g., “go to the blue chair in the kitchen”), and the generation step produces a sequence of actions or waypoints grounded in those retrieved facts. This design ensures that the generated plan is both contextually appropriate and causally consistent with the environment.

## Role in NavRAG

In the NavRAG framework, RAG retrieves relevant branches from a hierarchical tree of 3D scene descriptions. The tree encodes objects, their locations, and containment relationships (e.g., “mug on table in kitchen”). The retrieved sub‑tree is passed to an LLM to generate instructions that are both precise and varied. This decoupling allows the same scene representation to support multiple instruction styles without retraining.

---

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Pending review:**
- `Retrieval-Augmented Generation (RAG)` --related_to ⚠️ ⚠️--> `CausalNav` _(wikilink)_
- `Retrieval-Augmented Generation (RAG)` --related_to ⚠️ ⚠️--> `NavRAG` _(wikilink)_  
- `Retrieval-Augmented Generation (RAG)` --part_of ⚠️--> `NavRAG framework` _(wikilink)_