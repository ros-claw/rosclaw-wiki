---
id: gvnav
title: GVNav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:50:25'
last_reinforced: '2026-04-29T20:50:25'
supersedes: []
sources:
- papers/2502.19024.pdf
source_type: arxiv_paper
---

## GVNav

**GVNav** (Ground-View Navigation) is a vision-and-language navigation algorithm designed for quadruped robots with a low-height field of view. It addresses the perceptual challenges that arise when robots operate close to the ground, where visual obstructions and viewpoint mismatch degrade VLN performance. GVNav enriches spatiotemporal understanding by assigning weights to identical features observed across different viewpoints, leveraging historical observations to stabilize navigation in continuous environments.

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| Viewpoint height | Low-height field of view (ground-level) |
| Weight assignment | Assigns weights to identical features across different viewpoints based on historical observations |

### Capabilities

- Enables [[quadruped robots]] ⚠️ with low-height field of view to perform [[Vision-and-Language Navigation|VLN]] in continuous environments
- Overcomes visual obstructions and perceptual mismatches
- Improves performance in both simulated and real-world deployments

### Methodology

GVNav leverages weighted historical observations as enriched spatiotemporal contexts to manage feature collisions. It transfers connectivity graphs from [[HM3D]] and [[Gibson]] ⚠️ datasets to enhance spatial priors. The algorithm uses a [[waypoint predictor]] to generate candidate waypoints and then scores them using the weighted historical context, effectively compensating for the limited visual range of a ground-level camera.

{{uses: [[Weighted historical observations]] ⚠️ ⚠️, [[Connectivity graph from HM3D and Gibson]] ⚠️ ⚠️}}

{{depends_on: [[Vision-and-Language Navigation]] (VLN), [[Waypoint predictor]]}}

### Significance

GVNav is the first attempt to highlight the generalization gap in VLN across varying heights of visual observation in realistic robot deployments. By explicitly handling the mismatch between training (typically from higher viewpoints) and deployment (robot ground-level), it paves the way for more robust embodied navigation systems.

### Relationships

- **Uses** → [[Weighted historical observations]] ⚠️ ⚠️, [[Connectivity graph from HM3D and Gibson]] ⚠️ ⚠️
- **Depends on** → [[Vision-and-Language Navigation]] (VLN), [[Waypoint predictor]]
- **Related to** → [[Sim-to-real transfer]], [[Continuous Environment Navigation]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GVNav` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
- `GVNav` --[[extends]] ⚠️ ⚠️--> `waypoint predictor`
- `GVNav` --[[extends]] ⚠️ ⚠️--> `Waypoint predictor`
