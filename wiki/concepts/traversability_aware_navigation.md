---
id: traversability_aware_navigation
title: Traversability-aware navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:59:44'
last_reinforced: '2026-04-30T03:59:44'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Traversability-aware Navigation

**Traversability-aware navigation** is a paradigm in autonomous robot navigation that integrates terrain traversability evaluation directly into the path planning and control pipeline. Instead of relying solely on geometry-based costmaps or obstacle avoidance, this approach explicitly models the traversability of the terrain — i.e., how easily, safely, and stably a robot can move over a given surface — and uses that information to select optimal routes.

## Overview

Traditional navigation systems often treat all drivable areas as equally traversable, or they assign costs based only on surface slope or roughness. Traversability-aware navigation goes further by learning or estimating a continuous traversability metric from terrain properties (e.g., deformability, friction, obstacle density, dynamic stability) and incorporating that metric as a primary input to the planner. This enables robots to prefer paths that minimize risk, energy, or slippage, even if they are geometrically longer.

The concept is closely related to [[traversability estimation]] ⚠️, which provides the underlying terrain assessment, and to [[navigation costmaps]] ⚠️, which encode spatial costs for planning. Traversability-aware navigation can be implemented in both global and local planning layers.

## Capabilities

- **Navigation that considers terrain traversability in planning** – The path planner uses a traversability map (often learned from exteroceptive sensors like RGB-D cameras or LiDAR) to generate routes that minimise traversal risk and optimise for the robot’s dynamic capabilities.

## Relationship to TANGO

Traversability-aware navigation is a core design principle of the **[[TANGO]]** (Traversability-Aware Navigation for Ground robOts) system. TANGO explicitly implements traversability-aware planning at its foundation, using a learned traversability model to guide its local and global planners. This relationship can be annotated as:

- `[[TANGO]]` **depends_on** `[[Traversability-aware navigation]]`

## Related Concepts

- `[[Terrain traversability]] ⚠️`
- `[[Learning-based navigation]] ⚠️`
- `[[Safe navigation]]`
- `[[Costmap 2D]] ⚠️`

## Source

- ArXiv preprint 2509.08699 (2025): *TANGO: Traversability-Aware Navigation for Ground Robots*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Traversability-aware navigation` --[[related_to]] ⚠️--> `TANGO` _(wikilink)_
