---
id: llm_based_planner
title: LLM-based Planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:08:03'
last_reinforced: '2026-04-30T01:08:03'
supersedes: []
sources:
- papers/2410.06239.pdf
source_type: arxiv_paper
---

## LLM-based Planner

An **LLM-based Planner** is an algorithmic approach that leverages a Large Language Model (LLM) to generate and adapt navigation plans from natural language instructions. It operates within a Hierarchical Scene Graph Construction framework built on top of a Semantic Object Map ⚠️ ⚠️ ⚠️, enabling open-vocabulary reasoning about the environment.

### Input & Context

- **Input**: Navigation tasks specified in natural language (e.g., "go to the kitchen and bring the red cup").
- **Context**: Structured representations of the environment via hierarchical scene graphs extracted from a semantic object map. This provides both high-level spatial relationships and fine-grained object-level semantics.

### Capabilities

The LLM-based planner can:

- Generate multi‑step plans that decompose a natural language command into executable sequences of actions.
- Adapt plans in real time as the scene evolves (e.g., when objects are moved or obstacles appear), re‑planning without full reset.
- Use open‑vocabulary semantics, meaning it can handle arbitrary object labels and commands not seen during training.

### Dependencies

- **depends_on**: Hierarchical Scene Graph Construction and Semantic Object Map ⚠️ ⚠️ ⚠️ — these provide the symbolic grounding necessary for the LLM to reason about the physical world.

### Related Pages

- Large Language Models — the foundation of the planner.
- Semantic Navigation ⚠️ ⚠️ — the broader family of approaches that the LLM-based planner belongs to.
- Scene Graph ⚠️ — the representation format used to encode the environment.

### Relationship Annotations

- **implements** Semantic Navigation ⚠️ ⚠️ algorithms.
- **uses** Hierarchical Scene Graph Construction.
- **uses** Semantic Object Map ⚠️ ⚠️ ⚠️.
- **depends_on** both of the above.