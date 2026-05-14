---
id: scannet
title: ScanNet
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:53:09'
last_reinforced: '2026-04-29T21:53:09'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# ScanNet

**ScanNet** is a large-scale indoor scene dataset widely used for 3D scene understanding tasks. It provides RGB-D video sequences, 3D meshes, and semantic annotations for hundreds of real-world environments. In the embodied AI context, ScanNet serves as the foundation for the EmbodiedOcc-ScanNet Benchmark, a reorganized version with local annotations specifically designed to evaluate EmbodiedOcc’s embodied 3D occupancy prediction capabilities.

## Capabilities

- Supports evaluation of embodied 3D occupancy prediction by providing densely annotated local observations.

## Relationships

- **Used by** → EmbodiedOcc: The EmbodiedOcc model uses ScanNet (via the EmbodiedOcc-ScanNet benchmark) to train and assess its occupancy prediction on real indoor scenes.
- **Part of** → EmbodiedOcc-ScanNet Benchmark: ScanNet’s data is reorganized with local annotations to form this benchmark.

## EmbodiedOcc-ScanNet Benchmark

The EmbodiedOcc-ScanNet Benchmark is a reorganized subset of ScanNet that supplies **local annotations** — observations captured from an agent’s egocentric viewpoint — making it suitable for evaluating how well embodied occupancy prediction models generalize across traversed spaces. It is the primary dataset used by EmbodiedOcc for both training and testing.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ScanNet` --uses ⚠️--> `EmbodiedOcc`
