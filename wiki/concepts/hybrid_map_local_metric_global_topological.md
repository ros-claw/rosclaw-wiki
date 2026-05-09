---
id: hybrid_map_local_metric_global_topological
title: Hybrid Map (Local Metric + Global Topological)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:35:16'
last_reinforced: '2026-04-30T01:35:16'
supersedes: []
sources:
- papers/2212.04385.pdf
source_type: arxiv_paper
---

## Hybrid Map (Local Metric + Global Topological)

A **hybrid map** combines a [[Local Metric Map]] ⚠️ with a [[Global Topological Map]] ⚠️ to balance short-term spatial reasoning and long-term planning in [[Vision-Language Navigation]] (VLN). Proposed within the [[BEVBert]] framework, this representation explicitly aggregates incomplete, partial observations while maintaining a high‑level connectivity structure for path planning.

### Components

- **Local Metric Map** – Continuously aggregates incoming sensor data (e.g., RGB‑D, odometry) into a dense, metric representation of the immediate surroundings. Duplicate observations from visited poses are removed, yielding a consistent local occupancy estimate. This map supports reactive collision avoidance and fine‑grained obstacle reasoning.
- **Global Topological Map** – Models the navigation dependency between visited nodes (e.g., rooms, corridor intersections) as a graph. Edges encode connectivity (e.g., “door → kitchen”), enabling long‑horizon path planning and high‑level goal selection without precise metric pose.

### Purpose

The hybrid design explicitly addresses the tension between local precision and global abstraction:

- **Short‑term reasoning** – The local metric map handles immediate obstacle mapping and fine‑grained movement decisions.
- **Long‑term planning** – The global topological map enables the agent to reason about abstract routes, recall previously visited locations, and recover from local errors by re‑planning at the topological level.

### Capabilities

| Capability | Description |
|-----------|-------------|
| **Incomplete observation aggregation** | The local metric map fuses partial, noisy sensor readings into a single, coherent occupancy grid. |
| **Duplicate removal** | When the agent revisits a location, the metric map suppresses redundant observations, preventing overconfidence. |
| **Navigation dependency modeling** | The topological map captures ordering constraints (e.g., “must pass through hallway before reaching kitchen”), enabling structured exploration. |

### Relationships

- **Used by** → [[BEVBert]] – BEVBert’s architecture relies on this hybrid map to jointly train a Transformer‑based policy with both metric and topological priors.
- **Depends on** → [[Multimodal Map Representation]] ⚠️ – The hybrid map assumes a multimodal backbone (vision, language, occasionally depth) to populate its metric and topological structures. Without a unified feature space, the two maps cannot be aligned during training.

### Source

Introduced in the BEVBert paper (arXiv:2212.04385) as an explicit solution to the “short‑term vs. long‑term” trade‑off in VLN. The hybrid map is instantiated via separate encoder heads for metric and topological information, with a learned gating mechanism that decides when to rely on each layer.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Hybrid Map (Local Metric + Global Topological)` --[[related_to]] ⚠️--> `BEVBert` _(wikilink)_
