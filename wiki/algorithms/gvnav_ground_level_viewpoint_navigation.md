---
id: gvnav_ground_level_viewpoint_navigation
title: GVNav (Ground-level Viewpoint Navigation)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:09:08'
last_reinforced: '2026-04-30T00:09:08'
supersedes: []
sources:
- papers/2502.19024.pdf
source_type: arxiv_paper
---

# GVNav (Ground-level Viewpoint Navigation)

## Overview

GVNav (Ground-level Viewpoint Navigation) is an algorithm that addresses the **generalization gap in Vision-and-Language Navigation** caused by varying heights of visual observation, particularly for low-height robots. It leverages **weighted historical observations** as enriched spatiotemporal contexts and transfers connectivity graphs from HM3D and Gibson to improve spatial priors. This approach overcomes visual obstructions and perceptual mismatches encountered when an agent’s camera is positioned near the ground, significantly improving waypoint predictor generalization to real-world settings.

## Parameters

The algorithm uses two key parameters:

- **weighted_historical_observations**: `true` — Past observations are weighted and incorporated into the spatiotemporal context, providing richer navigation cues.
- **feature_collision_management**: `true` — Features are managed to avoid collisions and resolve occlusions common at low viewpoints.
- **connectivity_graph_transfer**: from HM3D and Gibson — Precomputed graph connectivity from these datasets is transferred to improve the spatial prior of the navigation model.

## Capabilities

GVNav enables the following:

- Improves VLN performance for low-height robots (e.g., small ground vehicles, quadrupedal robots).
- Overcomes visual obstructions and perceptual mismatches that arise from a ground-level viewpoint.
- Enhances waypoint predictor generalization to real-world scenes when trained on simulated data.

## Relationships

- **uses**: HM3D dataset, Gibson dataset, waypoint predictor
- **depends_on**: VLN, spatiotemporal context

## See Also

- Unitree G1 — Example robot platform that could benefit from low-height VLN.
- Embodied AI — Broader context for navigation and grounding.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GVNav (Ground-level Viewpoint Navigation)` --based_on ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `GVNav (Ground-level Viewpoint Navigation)` --extends ⚠️--> `waypoint predictor`
- `GVNav (Ground-level Viewpoint Navigation)` --implements ⚠️--> `Unitree G1`
- `GVNav (Ground-level Viewpoint Navigation)` --based_on ⚠️ ⚠️--> `Embodied AI`
