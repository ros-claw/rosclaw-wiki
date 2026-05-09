---
id: metric_aware_visual_geometry
title: Metric-aware visual geometry
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:23:19'
last_reinforced: '2026-04-30T03:23:19'
supersedes: []
sources:
- papers/2512.19629.pdf
source_type: arxiv_paper
---

# Metric-aware Visual Geometry

**Metric-aware visual geometry** refers to visual geometry processing that predicts absolute metric scale, enabling accurate spatial understanding without reliance on external localization systems (e.g., GPS or motion capture). By grounding visual predictions directly in real-world units, it allows robots to perceive geometry and robot state in metric terms from raw images.

## Capabilities

- Provides implicit state estimation for the robot, eliminating the need for separate localization modules.
- Grounds predictions with real-world scale, enabling direct transfer from perception to control.
- Supports dense geometry reconstruction for obstacle avoidance, crucial for navigation in cluttered environments.

## Relationships

- **Used by** → [[LoGoPlanner]]: The planner leverages metric-aware visual geometry to obtain reliable state and scene information.
- **Component of** → [[long-horizon visual-geometry backbone]]: Metric-aware visual geometry is a finetuned specialization of this backbone, enabling metric-scale reasoning from images.

## Role in LoGoPlanner

A long-horizon visual-geometry backbone is finetuned to become metric-aware, enabling the framework to estimate robot state and scene geometry in metric scale directly from images. This allows [[LoGoPlanner]] to plan and execute trajectories without external localization, relying solely on visual input for both state estimation and dense geometry reconstruction.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Metric-aware visual geometry` --[[related_to]] ⚠️ ⚠️--> `LoGoPlanner` _(wikilink)_
- `Metric-aware visual geometry` --[[related_to]] ⚠️ ⚠️--> `long-horizon visual-geometry backbone` _(wikilink)_
