---
id: object_level_topometric_navigation
title: Object-level topometric navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:59:01'
last_reinforced: '2026-04-30T03:59:01'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Object-level topometric navigation

**Object-level topometric navigation** is a paradigm for mobile robot navigation that represents goals as semantic object landmarks rather than raw metric coordinates or topological node sequences. It fuses the abstraction of topological navigation with the precision of metric approaches by anchoring waypoints to detected objects in the environment.

## Definition

In Object-level topometric navigation, goals are specified in terms of objects (e.g., "navigate to the chair" or "go to the table"). The robot maintains a topological graph where nodes are associated with object instances, and edges encode metric spatial relationships (poses, distances, orientations) between those objects. This hybrid representation allows the robot to reason about goals symbolically while executing precise metric motions.

## Capabilities

- **Represents navigation goals as object-level landmarks** – Instead of using a pre-built metric map or a purely topological list, the system defines key locations using recognized objects.
- **Combines topological and metric approaches** – The topological structure provides high-level route planning and robustness to perceptual aliasing, while the metric layer enables accurate local control and object-level localization.

## Relationship with TANGO

Object-level topometric navigation is used by TANGO, a system that "Tracks Anything and N Guidance with Objects." TANGO leverages object-level topometric representations to perform zero-shot navigation in unknown environments, using open-vocabulary object detection to instantiate landmarks on the fly and plan topological routes between them while executing metric movements.

## See also

- Topological navigation ⚠️
- Metric navigation ⚠️
- Object-goal navigation
- Zero-shot navigation
- TANGO (implements this concept)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Object-level topometric navigation` --related_to ⚠️--> `TANGO` _(wikilink)_
