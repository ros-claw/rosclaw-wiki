---
id: embodiedocc_scannet_benchmark
title: EmbodiedOcc-ScanNet Benchmark
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:40:06'
last_reinforced: '2026-04-30T04:40:06'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# EmbodiedOcc-ScanNet Benchmark

**EmbodiedOcc-ScanNet Benchmark** is a benchmark derived from the ScanNet dataset, reorganized with local annotations specifically designed to facilitate the evaluation of Embodied 3D Occupancy Prediction models in embodied AI contexts. It addresses the need for benchmarks that assess a robot’s ability to predict occupancy of its immediate surroundings from an egocentric perspective, rather than global scene-level reconstruction.

## Overview

The benchmark uses the ScanNet RGB-D dataset as its base and re-annotates scenes with **local occupancy labels** tailored for embodied evaluation. This focuses on the space directly around an agent’s viewpoint, enabling realistic testing of perception and prediction models that must operate with limited field-of-view and partial observability.

## Capabilities

- **Evaluates embodied 3D occupancy prediction** – measures how well a model predicts occupied vs. free space in the local vicinity of an agent, using metrics such as intersection-over-union (IoU) and precision/recall of occupancy grids.
- Provides a standardized evaluation protocol for methods in the EmbodiedOcc line of work.
- Enables fair comparison among approaches that estimate occupancy from a single camera frame or short trajectory.

## Dataset Parameters

| Parameter | Value |
|-----------|-------|
| Base dataset | ScanNet |
| Annotation focus | Local (egocentric) occupancy |
| Evaluation scope | Embodied prediction |

## Relationships

- **Depends on**: ScanNet (uses its scenes and original RGB-D sequences)
- **Used by**: EmbodiedOcc models (the benchmark is the primary evaluation platform for the EmbodiedOcc framework)
- **Related to**: Occupancy Prediction ⚠️, 3D Scene Understanding ⚠️, Embodied AI Benchmarks ⚠️

## Key Features

- Scans from ScanNet are partitioned into short, agent-centric **episodes** that simulate the visual input a robot would receive while navigating.
- Annotations are provided as local occupancy grids (e.g., 3D binary tensors) aligned to the camera coordinate frame at each timestep.
- The benchmark supports both **static** (single-frame) and **temporal** (multi-frame) occupancy prediction tasks, enabling evaluation of memory and temporal reasoning.

## Use in Embodied Setting

Unlike global occupancy benchmarks (e.g., Semantic Scene Completion ⚠️ on NYUv2 ⚠️), EmbodiedOcc-ScanNet prioritizes **egocentrism** and **partial observability**. This directly aligns with the needs of autonomous agents that must react to their immediate environment without full scene priors.

---

*See also: Occupancy Networks ⚠️, Neural Radiance Fields ⚠️, Sim-to-Real Transfer (for occupancy models deployed on real robots).*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EmbodiedOcc-ScanNet Benchmark` --applies_to ⚠️--> `ScanNet`
- `EmbodiedOcc-ScanNet Benchmark` --related_to ⚠️ ⚠️--> `Embodied 3D Occupancy Prediction`
**Pending review:**
- `EmbodiedOcc-ScanNet Benchmark` --related_to ⚠️ ⚠️--> `EmbodiedOcc` _(wikilink)_
