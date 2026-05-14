---
id: elevation_map_based_perception
title: Elevation Map-based Perception
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:40:08'
last_reinforced: '2026-04-29T21:40:08'
supersedes: []
sources:
- papers/2510.07152.pdf
source_type: arxiv_paper
---

## Description

**Elevation Map-based Perception** is a method in terrain perception that constructs a 2.5D grid map representing the height of the terrain at discrete cells. It uses depth sensors (e.g., Stereo Camera ⚠️, LiDAR) combined with Visual Odometry ⚠️ and IMU ⚠️-based localization to fuse successive measurements into a consistent elevation map. Historically, this approach has been a workhorse in traditional locomotion planning (e.g., for Legged Robots and rough-terrain navigation), but it incurs latency and robustness overhead due to the fusion of multiple sensor streams.

## Capabilities

- **Structured terrain representation**: Produces a geometric, quantized height field that can be directly fed into planners or traversability estimators.
- **Latency and fragility**: Sensor fusion delays and dependence on accurate localization make the pipeline slower and less robust than end-to-end methods.

## Dependencies

- **Multiple vision sensors**: Typically two or more imaging modalities (e.g., depth cameras, LiDAR, or stereo rigs).
- **Localization systems**: Requires high-frequency, drift-corrected odometry (e.g., Visual-Inertial Odometry ⚠️ or GPS ⚠️) to align successive depth measurements.

## Relationships

- **Used by**: Terrain-Aware Locomotion Policy with a Blind Backbone — this approach augments a blind policy with an elevation map to improve adaptability.
- **Alternative to**: Depth image-based end-to-end learning ⚠️ — the end-to-end method skips explicit map building and instead learns directly from depth images, trading structure for speed.

## References

- Source: *Terrain-Aware Locomotion Policy with a Blind Backbone* (arxiv 2510.07152).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Elevation Map-based Perception` --applies_to ⚠️--> `Legged Robots`
**Pending review:**
- `Elevation Map-based Perception` --related_to ⚠️--> `Terrain-Aware Locomotion Policy with a Blind Backbone` _(wikilink)_
