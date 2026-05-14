---
id: embodiedocc_scannet
title: EmbodiedOcc-ScanNet
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T04:45:31'
last_reinforced: '2026-04-30T04:45:31'
supersedes: []
sources:
- papers/2504.14604.pdf
source_type: arxiv_paper
---

# EmbodiedOcc-ScanNet

**EmbodiedOcc-ScanNet** is a large-scale egocentric occupancy dataset derived from the ScanNet indoor scene dataset. It is designed specifically for evaluating and training embodied occupancy prediction models, providing dense ground-truth occupancy annotations from an agent's first-person perspective.

As a dataset, EmbodiedOcc-ScanNet serves as a primary evaluation benchmark for the RoboOcc framework, which leverages embodied occupancy representations for robot manipulation and navigation. The dataset captures realistic indoor environments with full 3D scene geometry, enabling research in sim-to-real transfer and embodied AI.

## Key Characteristics

- **Source**: Processed from ScanNet RGB-D scans.
- **Type**: Egocentric occupancy grid dataset.
- **Scale**: Covers thousands of frames across multiple indoor scenes.
- **Annotations**: Voxel-level occupancy labels relative to the agent's current viewpoint.

## Usage

EmbodiedOcc-ScanNet is used to train and evaluate occupancy prediction models that operate on partial sensor observations. It is the core dataset behind the experiments reported in the paper associated with RoboOcc (arXiv:2504.14604).

## Relationships

- **used_by**: RoboOcc — This dataset is the primary benchmark for RoboOcc's occupancy prediction pipeline.
- **type**: Dataset — It provides structured occupancy data for embodied AI research.
- **depends_on**: ScanNet — Inherits scene geometry and camera trajectories from the original ScanNet dataset.

## Related Concepts

- EmbodiedOcc – The broader task of predicting occupancy from an agent's perspective.
- Occupancy Grid ⚠️ – The representation format used in the dataset.

## See Also

- Sim-to-Real Transfer – The dataset supports sim-to-real evaluation.
- Embodied AI – EmbodiedOcc-ScanNet contributes to the embodied intelligence paradigm.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EmbodiedOcc-ScanNet` --depends_on ⚠️--> `ScanNet`
- `EmbodiedOcc-ScanNet` --uses ⚠️ ⚠️--> `RoboOcc`
- `EmbodiedOcc-ScanNet` --uses ⚠️ ⚠️--> `EmbodiedOcc`
- `EmbodiedOcc-ScanNet` --related_to ⚠️--> `Embodied AI`
