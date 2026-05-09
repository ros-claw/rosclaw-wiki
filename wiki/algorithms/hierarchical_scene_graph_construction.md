---
id: hierarchical_scene_graph_construction
title: Hierarchical Scene Graph Construction
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:08:39'
last_reinforced: '2026-04-30T01:08:39'
supersedes: []
sources:
- papers/2410.06239.pdf
source_type: arxiv_paper
---

# Hierarchical Scene Graph Construction

**Hierarchical Scene Graph Construction** is an algorithm that builds structured, hierarchical representations of an environment from onboard sensory data and open-vocabulary semantics. It consumes a continuously updated semantic object map and produces a layered scene graph that captures spatial, functional, and semantic relations among objects and regions.

## Overview

Traditional scene graphs flatten object relationships. This algorithm constructs multiple layers – from low-level object instances to higher-level regions, rooms, and functional zones – allowing an agent to reason at varying levels of abstraction. The hierarchy is built incrementally; as new observations arrive, the graph is updated to reflect changes in the environment.

## Input and Output

| Aspect | Description |
|--------|-------------|
| **Input**  | Onboard sensory data (RGB-D, LiDAR, etc.) combined with open-vocabulary semantics (e.g., object categories, attributes) |
| **Output** | A hierarchical scene graph derived from a continuously updated [[Semantic Object Map]] ⚠️ ⚠️ ⚠️ |

## Capabilities

- **Incremental construction**: Scene graphs are built and refined online as the agent explores the environment.
- **Open-vocabulary support**: Objects and regions are labeled with natural language concepts, enabling flexible reasoning.
- **Continuous updating**: The graph evolves to reflect changes in object positions, appearances, and relationships.

## Usage

This algorithm is used by the [[LLM-based Planner]] to generate context-aware navigation and manipulation plans. The planner queries the hierarchical scene graph for spatial relations, containment, and affordances, enabling grounded action selection.

## Related Concepts

- [[Semantic Object Map]] ⚠️ ⚠️ ⚠️ – The underlying map from which the scene graph is derived.
- [[Scene Graph]] ⚠️ – General representation of objects and their relationships.
- [[LLM-based Planner]] – Downstream component that consumes the graph for task planning.

## Relationship Annotations

- `[[Hierarchical Scene Graph Construction]]` **depends_on** `[[Semantic Object Map]] ⚠️ ⚠️ ⚠️`
- `[[LLM-based Planner]]` **uses** `[[Hierarchical Scene Graph Construction]]`