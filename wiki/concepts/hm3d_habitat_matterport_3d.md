---
id: hm3d_habitat_matterport_3d
title: HM3D (Habitat Matterport 3D)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:38:27'
last_reinforced: '2026-04-29T20:38:27'
supersedes: []
sources:
- papers/2509.16445.json
source_type: arxiv_paper
---

# HM3D (Habitat Matterport 3D)

**HM3D** (Habitat Matterport 3D) is a large-scale benchmark dataset of photorealistic 3D indoor environments reconstructed from real-world Matterport scans. It is widely used for evaluating embodied navigation tasks within the [[Habitat Simulator]] ecosystem.

## Overview

HM3D provides 90+ high-fidelity, semantically annotated scenes spanning diverse residential and commercial interiors (e.g., homes, offices, hotels). Each scene is a fully textured 3D mesh with navigable free space, enabling realistic agent simulation. The dataset is designed to bridge the gap between synthetic and real-world embodied AI evaluation.

## Key Properties

- **Type:** Benchmark dataset
- **Domain:** Realistic 3D indoor environments
- **Size:** ~90 scenes (split into train/val/test)
- **Annotation:** Semantic object labels (e.g., chairs, tables, beds), navigable meshes, episode definitions for standard tasks

## Capabilities

- Provides realistic 3D indoor environments for navigation evaluation, particularly for tasks requiring visual grounding and generalization to diverse floor plans.
- Supports both **ObjectNav** (finding a specific object category) and **OVON** (open-vocabulary object navigation) tasks.
- Enables sim-to-real transfer research by offering high visual fidelity and real-world clutter.

## Relationships

- **Used by** [[FiLM-Nav]] for evaluation on [[ObjectNav]] and [[OVON]] tasks.
- Part of the ecosystem of datasets supported by [[Habitat Simulator]] and [[Habitat Lab]] ⚠️.
- Depends on **Matterport 3D** sensor data (RGB-D, mesh) captured from real-world scans.

## Usage in Research

HM3D is the primary evaluation benchmark in the [[Habitat Challenge]] ⚠️ competitions. Researchers use it to test navigation policies trained in simulation, then transfer to real robots. The dataset's realism helps assess generalization beyond simple synthetic environments like [[Gibson]] ⚠️ or [[Matterport3D]] ⚠️.

## See Also

- [[ObjectNav]] – Task of navigating to an object instance by category.
- [[OVON]] – Open-vocabulary object navigation.
- [[Habitat Simulator]] – Platform for embodied agent simulation.
- [[FiLM-Nav]] – Model that uses language-conditioned visual features for navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `HM3D (Habitat Matterport 3D)` --[[related_to]] ⚠️--> `FiLM-Nav` _(wikilink)_
