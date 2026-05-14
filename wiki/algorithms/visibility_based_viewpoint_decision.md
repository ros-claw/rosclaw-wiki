---
id: visibility_based_viewpoint_decision
title: Visibility-based Viewpoint Decision
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:46:55'
last_reinforced: '2026-04-30T03:46:55'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

## Visibility-based Viewpoint Decision

**Visibility-based Viewpoint Decision** is an algorithm that explicitly addresses the Last Mile Problem ⚠️ ⚠️ ⚠️ in Zero-Shot Navigation. It determines a feasible target location along with a suitable final viewpoint, ensuring that the navigable path ends at a position where the target object is visible and reachable.

### Description

The algorithm resolves the last mile challenge by evaluating candidate viewpoints based on visibility constraints. Instead of merely planning a path to a predicted location, it reasons about whether the final position provides an unobstructed line of sight to the target. This is critical for zero-shot navigation where no prior exploration or scene-specific training is available.

### Capabilities

- **Last-resort viewpoint selection:** identifies a feasible target location with a suitable final viewpoint by analyzing visibility from candidate positions.
- **Integration with navigation policies:** works in tandem with higher-level planners to ensure that the final step of the path satisfies visual and geometric constraints.
- **Zero-shot applicability:** requires no fine-tuning on the target environment, making it generalizable to unseen spaces.

### Relationships

- **part_of** MSGNav — Visibility-based Viewpoint Decision is a component of the MSGNav pipeline, handling the terminal stage of navigation.
- **depends_on** Last Mile Problem formulation — the algorithm directly solves this known difficulty in goal-oriented navigation.
- **implements** Zero-Shot Navigation principles by using only geometric and visibility reasoning without environment-specific training.
- **uses** Viewpoint Planning ⚠️ ⚠️ concepts to rank candidate positions.

### Related Concepts

- MSGNav
- Zero-Shot Navigation
- Viewpoint Planning ⚠️ ⚠️
- Last Mile Problem ⚠️ ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visibility-based Viewpoint Decision` --extends ⚠️--> `MSGNav`
