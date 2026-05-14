---
id: long_horizon_visual_geometry_backbone
title: Long-horizon Visual-geometry Backbone
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:29:46'
last_reinforced: '2026-04-29T21:29:46'
supersedes: []
sources:
- papers/2512.19629.pdf
source_type: arxiv_paper
---

# Long-horizon Visual-geometry Backbone

## Description

The **Long-horizon Visual-geometry Backbone** is an algorithmic component that processes sequences of visual observations over an extended time horizon. It produces metric-aware geometric hidden representations that enable grounding of predictions with absolute metric scale. This backbone serves as the perceptual foundation for tasks requiring implicit state estimation and accurate localization.

## Capabilities

- **Implicit state estimation**: The backbone infers robot or scene state directly from visual data without explicit state filters.
- **Metric scale grounding**: Output features carry absolute metric information, enabling precise localization and planning in real-world coordinates.

## Parameters

| Parameter | Detail |
|-----------|--------|
| **Role** | Provides hidden representation for grounding predictions with absolute metric scale |
| **Training** | Finetuned with auxiliary tasks (e.g., metric scale and geometry objectives) |

## Relationships

- **Used by**: LoGoPlanner – this backbone feeds metric-aware features into the planner for long-horizon navigation.
- **Depends on**: Visual observations (e.g., camera streams), auxiliary tasks that enforce metric scale and geometric consistency during training.

## Training & Integration

During training, the backbone is finetuned with auxiliary losses that encourage the hidden representation to encode metric-scale geometry. At inference time, the backbone consumes raw visual observations and outputs features that LoGoPlanner can directly use for grounding predictions without additional scale estimation modules.

## Related Topics

- Visual-geometry Backbones ⚠️ (broader category)
- Metric Scale Grounding ⚠️
- Implicit State Estimation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Long-horizon Visual-geometry Backbone` --extends ⚠️--> `LoGoPlanner`
