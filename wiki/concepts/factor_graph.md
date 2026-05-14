---
id: factor_graph
title: Factor Graph
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:56:07'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Factor Graph

A **Factor Graph** is a type of **probabilistic graphical model** used to represent dependencies between variables through factor nodes. In the context of robotics and mapping, factor graphs enable robot pose and landmark estimation by jointly modeling observations and constraints in a graph structure.

## Definition

A factor graph is a probabilistic graphical model that represents the joint distribution of robot poses and landmark positions, enabling simultaneous localization and mapping (SLAM). It constructs a 3D graph of landmarks estimated jointly with robot poses, making it particularly effective for mapping large-scale scenes such as multifloor homes.

## Parameters

- **Type**: Probabilistic graphical model
- **Technique**: 3D graph of landmarks estimated jointly with robot poses
- **Application**: Mapping large‑scale scenes with a 3D graph of landmarks estimated jointly with robot poses. This approach is particularly effective for Simultaneous Localization and Mapping tasks, including robustly and efficiently mapping multifloor homes by capturing spatial constraints across levels.

## Capabilities

- Robust and efficient mapping of large‑scale environments, such as multifloor homes, by capturing spatial constraints across levels.
- Enable graph‑based landmark estimation, improving consistency in long‑term navigation.
- Widely adopted in commercial robots, including drones and robot vacuums, for real‑time mapping and localization.

## Relationships

- **Used by**: Language-Inferred Factor Graph for Instruction Following (LIFGIF) – LIFGIF extends the factor graph paradigm to incorporate language grounding for zero‑shot instruction following.
- **Used by**: Commercial robots such as drones and robot vacuums rely on factor graphs for real‑time mapping and localization.

## In Context of LIFGIF

LIFGIF extends the factor graph approach by inferring language grounding within the graph structure for zero‑shot instruction following. This allows a robot to interpret natural‑language commands and plan trajectories directly from the factor graph’s inferred landmarks and spatial relations, without requiring task‑specific training data.

## See Also

- Probabilistic Graphical Model ⚠️
- Robot Pose Estimation ⚠️
- Zero-Shot Instruction Following

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Factor Graph` --related_to ⚠️--> `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` _(wikilink)_