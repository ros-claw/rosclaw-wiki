---
id: self_occlusion_aware_ray_casting
title: Self-Occlusion-Aware Ray Casting
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:41:22'
last_reinforced: '2026-04-29T21:41:22'
supersedes: []
sources:
- papers/2510.07152.pdf
source_type: arxiv_paper
---

# Self-Occlusion-Aware Ray Casting

## Overview

Self-Occlusion-Aware Ray Casting is a technique used in synthetic depth image generation that explicitly models the occlusion of the camera's line-of-sight by the robot's own body parts. Unlike naive [[Ray Casting]] ⚠️ ⚠️ methods that assume the robot's geometry is invisible to its own onboard cameras, this approach accurately renders depth shadows caused by the robot's limbs, torso, or other components. This yields significantly more realistic depth observations for simulation-based training and evaluation.

## Description

In typical sim-to-real pipelines, rendering depth from a camera mounted on a robot often ignores the fact that parts of the robot itself can block the view of the environment. Self-Occlusion-Aware Ray Casting corrects this by performing ray casting from the camera's origin and checking for intersections not only with the environment but also with the robot's own kinematic chain and surface geometry. The resulting depth image contains realistic occluded regions that match what a real sensor would produce, reducing the domain gap between simulation and reality.

## Capabilities

- Accounts for self-occlusion when rendering depth images in simulation
- Improves realism of synthetic depth observations, especially for cameras mounted on manipulator arms or humanoid robots

## Relationships

- **Part of** [[Realistic Depth Images Synthetic Method]] – a broader methodology for creating lifelike synthetic depth data.
- **Related to** [[Ray Casting]] ⚠️ ⚠️ and [[Depth Rendering]] ⚠️ – builds upon these base techniques by adding self-occlusion handling.

## See Also

- [[Sim-to-Real Transfer]]
- [[Domain Randomization]] ⚠️ (often combined with realistic rendering)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Self-Occlusion-Aware Ray Casting` --[[related_to]] ⚠️--> `Realistic Depth Images Synthetic Method` _(wikilink)_
