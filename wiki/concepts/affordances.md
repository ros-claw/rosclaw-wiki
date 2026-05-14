---
id: affordances
title: Affordances
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:53:56'
last_reinforced: '2026-04-30T00:53:56'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# Affordances

**Affordances** are navigational possibilities derived from visible ground segmentation. In the context of navigation, they specify where and how a robot can move by directly interpreting the traversable surface geometry from perceptual input. This concept bridges perception and action: it translates raw sensor data into actionable movement primitives without requiring explicit semantic mapping.

## Key Properties

- **Context**: Navigation
- **Definition**: Navigational affordances derived from visible ground segmentation
- **Capabilities**:
  - Enables zero-shot motion planning — the robot can decide where to move without task-specific training
  - Bridges perception and action — directly links visual understanding to motor commands

## Relationships

- `associated_with` — Visual Affordances Prompting ⚠️ ⚠️, which uses affordances as the key intermediate representation for grounding language commands in traversable space.
- `associated_with` — AO-Planner, a system that plans motion over affordance maps extracted from visual inputs.
- `implements` — a functional mapping from visual observation to relative action feasibility.
- `uses` — ground segmentation as the primary perceptual bottleneck.

## Role in Embodied AI

Affordances simplify the perception-action loop: instead of building a full 3D geometric map or object-level scene graph, the robot only needs to segment the visible ground surface and label each pixel with its immediate navigational consequence (e.g., “walkable”, “step-over”, “obstacle”). This makes motion planning computationally cheap and generalizable across environments — a core insight behind Visual Affordances Prompting ⚠️ ⚠️.

In the AO-Planner architecture, affordances serve as the action space itself: the planner directly selects affordance instantiations (e.g., “move to that walkable patch”) rather than computing waypoints in continuous coordinates. This tight coupling between perception and action is what enables zero-shot deployment without fine-tuning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Affordances` --related_to ⚠️--> `AO-Planner` _(wikilink)_
