---
id: system_2
title: System 2
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:20:15'
last_reinforced: '2026-04-30T00:20:15'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# System 2

**System 2** is a **VLM-based global planner** that serves as the high-level reasoning module within the [[DualVLN]] architecture. It predicts mid-term waypoint goals by performing image-grounded reasoning over the visual environment.

## Overview

System 2 is responsible for deliberative, slow grounding of visual observations into abstract waypoint goals. Unlike rapid reactive modules, it reasons about the overall trajectory to produce sparse, high-level subgoals. These goals are then passed to [[System 1]] for low-level execution.

## Capabilities

- **High-level reasoning**: Understands spatial layout and object relationships from images.
- **Grounding slowly**: Processes visual context deliberately to emit stable, mid-term navigation targets.

## Relationships

| Relation | Entity | Description |
|----------|--------|-------------|
| part_of | [[DualVLN]] | System 2 is a core component of the DualVLN framework. |
| provides_input_to | [[System 1]] | System 2 outputs waypoint goals that System 1 uses for fine-grained motion control. |

System 2 uses a [[Vision-Language Model (VLM)]] to encode visual scenes and reason about navigation goals. Its predictions are temporally sparse (mid-term) and act as a bridge between high-level task objectives and low-level actions.

## References

- Source paper: [[2512.08186.pdf]] ⚠️ (DualVLN: …) – details System 2's design and integration within the two‑system architecture.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `System 2` --[[uses]] ⚠️--> `DualVLN`
- `System 2` --[[related_to]] ⚠️--> `Vision-Language Model (VLM)`
