---
id: bsg_bev_scene_graph
title: BSG (BEV Scene Graph)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:10:05'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2308.04758.pdf
source_type: arxiv_paper
---

# BSG (BEV Scene Graph)

**BSG (BEV Scene Graph)** is a multi-step algorithm for vision-and-language navigation in indoor environments. It leverages multi-step BEV representations under 3D detection ⚠️ ⚠️ ⚠️ supervision to encode scene layouts and geometric cues. At each navigation step, a local local BEV representation ⚠️ is built from the agent’s current view, and a global scene map ⚠️ stores these local representations organized by topological relations derived from the agent’s path.

## Capabilities

- Encode scene layouts and geometric cues of indoor environment ⚠️ ⚠️s
- Maintain a BEV-based global scene map with topological relations between visited locations
- Predict a **local BEV grid-level decision score** from the current local BEV
- Predict a **global graph-level decision score** by reasoning over the stored topological scene graph
- Combine a **sub-view selection score** evaluated on panoramic observations ⚠️ ⚠️ to refine action candidates
- Improve action prediction accuracy over prior systems

## Parameters

- **Representation**: multi-step BEV representations
- **Supervision**: 3D detection ⚠️ ⚠️ ⚠️
- **Map structure**: local BEV at each step and global scene map with topological relations

## Relationships

| Relation       | Target(s)                                                                 |
|----------------|---------------------------------------------------------------------------|
| `uses`         | 3D detection ⚠️ ⚠️ ⚠️, panoramic observations ⚠️ ⚠️                              |
| `depends_on`   | indoor environment ⚠️ ⚠️, 3D scene geometry ⚠️                             |
| `evaluated_on` | REVERIE, R2R, R4R ⚠️ ⚠️ benchmarks                                  |
| `outperforms`  | Prior methods on REVERIE, R2R, R4R; state-of-the-art VLN methods          |

## Method

The algorithm builds a **local BEV** at each navigation step from the agent’s current panoramic observations. These local BEV grids are aggregated into a **global scene map** organized as a topological graph, where nodes correspond to visited locations and edges encode spatial relations (derived from the agent’s trajectory).

Action prediction fuses three scores:

1. **Local BEV grid-level decision score** – computed directly from the current local BEV.
2. **Global graph-level decision score** – obtained by reasoning over the stored topological scene graph.
3. **Sub-view selection score** – evaluated on the set of panoramic observations available at the current node.

These scores are combined to select the action with the highest overall utility.

## Evaluation

BSG significantly outperforms state-of-the-art methods on the REVERIE, R2R, and R4R ⚠️ ⚠️ benchmarks. Its ability to maintain a persistent geometric memory and jointly reason at local and global scales yields substantial gains in navigation success rates and goal-reaching accuracy.