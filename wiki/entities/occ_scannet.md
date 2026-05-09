---
id: occ_scannet
title: Occ-ScanNet
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T04:44:42'
last_reinforced: '2026-04-30T04:44:42'
supersedes: []
sources:
- papers/2504.14604.pdf
source_type: arxiv_paper
---

## Occ-ScanNet

**Occ-ScanNet** is a large-scale 3D occupancy prediction dataset designed to support embodied intelligence research in real-world environments. It provides dense volumetric occupancy annotations with semantic labels, enabling models to understand both geometry and semantics of complex scenes.

The dataset was introduced in the paper *"RoboOcc: A Semantic Robotic Occupancy Prediction Framework for Efficient and Scalable Deployment"* (arXiv:2504.14604). It serves as a key training and evaluation resource for the [[RoboOcc]] framework.

### Details
- **Type**: Dataset
- **Domain**: 3D semantic occupancy prediction
- **Annotations**: Voxel-level occupancy with semantic labels
- **Source**: Real-world scans (derived from [[ScanNet]] v2 data, extended with occupancy ground truth)
- **Key characteristics**:
  - Covers a variety of indoor scenes
  - Provides camera poses, RGB-D streams, and occupancy grids
  - Compatible with [[SparseVoxel]] ⚠️ and [[SemanticKITTI]] evaluation protocols

### Relationship
- **Used by** → [[RoboOcc]]: Occ-ScanNet is the primary dataset used for training and benchmarking the RoboOcc occupancy prediction framework.

### Usage
Researchers working on embodied AI, robotic navigation, and scene understanding can use Occ-ScanNet to develop and test occupancy prediction models. It is particularly suited for sim-to-real transfer and real-time deployment on robotic platforms such as [[Unitree G1]].

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Occ-ScanNet` --[[uses]] ⚠️--> `RoboOcc`
- `Occ-ScanNet` --[[depends_on]] ⚠️ ⚠️--> `ScanNet`
- `Occ-ScanNet` --[[depends_on]] ⚠️ ⚠️--> `Unitree G1`
