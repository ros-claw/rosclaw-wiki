---
id: connectivity_graph
title: Connectivity Graph
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:22:27'
last_reinforced: '2026-04-30T02:22:27'
supersedes: []
sources:
- papers/2203.02764.pdf
source_type: arxiv_paper
---

## Connectivity Graph

A **Connectivity Graph** represents the navigable connections between waypoints in an environment. In the context of discrete Vision-and-Language Navigation (VLN), the agent assumes full knowledge of this graph to jump between nodes, rather than executing low‑level motor commands.

### Overview

The connectivity graph is a directed or undirected graph where vertices correspond to reachable waypoints (e.g., panoramic viewpoints) and edges denote traversable paths between them. It provides the discrete action space for navigation agents: at each step, the agent selects an adjacent node from the graph to move to.

This graph is central to **discrete VLN** benchmarks such as R2R and RxR, where the environment is pre‑built from scans and the graph is derived from that geometry.

### Refinement

The structured facts indicate that the connectivity graph used in the source paper was refined:

- **Refined from:** Matterport3D ⚠️ ⚠️ ⚠️
- **Refined to:** Habitat-Matterport3D ⚠️ ⚠️ ⚠️

This refinement likely involved merging overlapping scans, fixing connectivity errors, and producing a cleaner, more consistent graph for training and evaluation. The resulting graph is used as training data for the Waypoints Predictor ⚠️ ⚠️ ⚠️ ⚠️.

### Capabilities

- Provides navigable nodes for **discrete navigation** — the agent can only move between pre‑defined waypoints.
- Serves as ground‑truth connectivity when training the Waypoints Predictor ⚠️ ⚠️ ⚠️ ⚠️ to predict likely nodes from visual inputs.

### Relationships

| Relation | Target |
|----------|--------|
| `depends_on` | Matterport3D ⚠️ ⚠️ ⚠️, Habitat-Matterport3D ⚠️ ⚠️ ⚠️ |
| `used_by` | Waypoints Predictor ⚠️ ⚠️ ⚠️ ⚠️ |
| `part_of` | Vision-and-Language Navigation pipeline |
| `implements` | Discrete navigation action space |

### Related Pages

- Matterport3D ⚠️ ⚠️ ⚠️ — original 3D scan dataset.
- Habitat-Matterport3D ⚠️ ⚠️ ⚠️ — refined version used in Habitat simulator.
- Waypoints Predictor ⚠️ ⚠️ ⚠️ ⚠️ — learns to predict connectivity graph nodes from visual observations.
- Discrete Navigation ⚠️ — paradigm in which agents operate over a fixed graph.
- Continuous Navigation ⚠️ — alternative where agents act in free space without a pre‑defined graph.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Connectivity Graph` --related_to ⚠️--> `Vision-and-Language Navigation`
