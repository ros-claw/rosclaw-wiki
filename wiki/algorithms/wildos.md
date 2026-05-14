---
id: wildos
title: WildOS
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:34:23'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2602.19308.json
- articles/wildos.md
source_type: arxiv_paper
---

## Overview

**WildOS** is a unified algorithm for long-range, open-vocabulary object search by mobile robots in unstructured outdoor environments. It enables autonomous navigation to distant, semantically specified targets across complex off-road and urban terrains without requiring prior maps. By combining a sparse topological memory with vision foundation models and probabilistic localization, WildOS bridges the gap between semantic reasoning and geometric safety over 100+ meter distances.

## Parameters

| Parameter | Value |
|-----------|-------|
| **Type** | Unified system for long-range open-vocabulary object search |
| **Inputs** | Depth images, RGB images, open-vocabulary query |
| **Outputs** | Navigation commands to the target object |
| **Modules** | ExploRFM, Particle Filter Coarse Localization, Sparse Navigation Graph ⚠️ ⚠️ ⚠️ ⚠️, Hierarchical Planner |
| **Vision Module** | ExploRFM |
| **Goal Localization** | Particle Filter ⚠️ ⚠️ (probabilistic triangulation) |
| **Planner** | Hierarchical Planner |

## Capabilities

- Open-vocabulary object search in unstructured outdoor environments
- Long-range semantic navigation (100+ m) without prior maps
- Real-time onboard semantic reasoning using vision foundation models
- Combines geometric safety via frontier exploration with visual-semantic cues
- Coarse localization of distant goals beyond depth sensor range
- Robust operation in off-road and urban terrains

## Method Overview

WildOS consists of five integrated components:

1. **Sparse Navigation Graph Construction** – builds a topological memory of traversable space using depth and odometry.
2. **ExploRFM Vision Module** – computes visual traversability, identifies frontiers, and evaluates visual similarity to the query using foundation models.
3. **Probabilistic Goal Triangulation via Particle Filter** – fuses multiple observations to estimate the location of the target object, even when the object is beyond the depth sensor range.
4. **Frontier Node Scoring** – combines geometric frontier exploration with visual-semantic cues from ExploRFM to prioritize promising regions.
5. **Hierarchical Planning** – uses a Hierarchical Planner to generate safe, efficient navigation commands toward the estimated goal.

## System Architecture

WildOS combines a **Sparse Navigation Graph ⚠️ ⚠️ ⚠️ ⚠️** for spatial memory with **ExploRFM**, a foundation-model-based vision module that scores frontier nodes. A **Particle Filter Coarse Localization** then probabilistically triangulates candidate goal positions for the target open-vocabulary query, extending the robot's perception horizon beyond its depth sensor range. The Hierarchical Planner orchestrates exploration and goal‑directed navigation, ensuring both semantic awareness and geometric safety. This architecture allows the system to maintain a rough mental map while focusing exploration on semantically promising regions.

## Key Insight

WildOS integrates language grounding (via vision foundation models), vision-based probabilistic localization (via particle filter), and geometric planning (via frontier exploration) to enable end-to-end open-vocabulary object search. The system operates in real time on a deployed robot platform, linking high‑level semantic goals to low‑level control without prior maps.

## Experimental Results

In field experiments across off-road and urban terrains, WildOS significantly outperformed purely geometric and purely vision-based baselines in both efficiency (time to locate target) and autonomy (reduced human interventions). The system demonstrated consistent ability to locate objects described by open-vocabulary queries such as “a red mailbox” or “a blue dumpster” from over 150 meters away, even when the object was completely outside the camera's initial field of view.

## Relationships

- **Uses:** ROS2, ExploRFM, Particle Filter ⚠️ ⚠️, Hierarchical Planner, Sparse Navigation Graph ⚠️ ⚠️ ⚠️ ⚠️
- **Depends On:** Vision Foundation Models ⚠️ ⚠️, Depth Sensing ⚠️ ⚠️, Geometric Frontier Exploration ⚠️ ⚠️
- **Implements:** Open-Vocabulary Object Search (long-range variant)

## See Also

- ExploRFM – vision foundation module used by WildOS
- Particle Filter Coarse Localization – probabilistic goal estimation component
- Sparse Navigation Graph ⚠️ ⚠️ ⚠️ ⚠️ – topological memory structure
- Hierarchical Planner – navigation planner used in WildOS
- Vision Foundation Models ⚠️ ⚠️ – backbone for open-vocabulary understanding
- Depth Sensing ⚠️ ⚠️ – sensor modality for geometric safety
- Geometric Frontier Exploration ⚠️ ⚠️ – safety‑guaranteed exploration strategy
- Open-Vocabulary Object Search – the general problem WildOS solves

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `WildOS` --extends ⚠️ ⚠️--> `ExploRFM`
- `WildOS` --extends ⚠️ ⚠️--> `Particle Filter Coarse Localization`
- `WildOS` --based_on ⚠️--> `Open-Vocabulary Object Search`