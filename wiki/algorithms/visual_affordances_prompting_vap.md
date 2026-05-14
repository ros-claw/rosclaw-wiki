---
id: visual_affordances_prompting_vap
title: Visual Affordances Prompting (VAP)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:20'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# Visual Affordances Prompting (VAP)

**Visual Affordances Prompting (VAP)** is an algorithm that leverages SAM ⚠️ ⚠️ ⚠️ ⚠️ (Segment Anything Model) to segment the **visible ground** in an image, extracting **navigational affordances** (walkable areas, obstacles, pathways). These affordances are then used to prompt a Large Language Model (LLM) to select candidate waypoints and generate low-level motion plans.

VAP forms a core component of the AO-Planner architecture, bridging vision and language for robot navigation in unstructured environments.

## Method

The visible ground in the robot’s camera view is segmented by SAM ⚠️ ⚠️ ⚠️ ⚠️ into affordance regions (e.g., traversable, avoidable). This segmentation provides a structured set of **navigational affordances**, which are represented as spatial prompt tokens. The LLM ⚠️ ⚠️, conditioned on the affordance prompt and a natural language instruction, selects the most suitable waypoints and plans a low-level path that respects the environment’s traversability constraints.

## Capabilities

- Segments the visible ground plane using SAM ⚠️ ⚠️ ⚠️ ⚠️ to produce a set of navigational affordances.
- Enables an LLM ⚠️ ⚠️ to reason over these affordances and **generate candidate waypoints**.
- Provides the basis for **low-level path planning towards waypoints**, converting high‑level language instructions into feasible trajectories.

## Relationships

- **uses** → SAM ⚠️ ⚠️ ⚠️ ⚠️ for segmentation
- **part_of** → AO-Planner (the integrated planning system)

For related work, see also Affordance-Based Planning ⚠️, Visual Grounding for Robotics ⚠️, and LLM-Based Waypoint Selection ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visual Affordances Prompting (VAP)` --extends ⚠️--> `AO-Planner`