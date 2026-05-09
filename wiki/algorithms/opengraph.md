---
id: opengraph
title: OpenGraph
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:38:29'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2403.09412.pdf
- papers/2403.09412.json
source_type: arxiv_paper
---

# OpenGraph

OpenGraph is the first **open-vocabulary hierarchical 3D graph representation** algorithm for large-scale outdoor environments. It combines [[Visual-Language Model (VLM)]] ⚠️ reasoning with [[LiDAR]] to create a semantically rich, scalable map. Introduced in the paper “OpenGraph: Open-Vocabulary Graph Construction for Large-Scale Outdoor Environments” (arXiv:2403.09412), it achieves state‑of‑the‑art segmentation and query accuracy on the [[SemanticKITTI]] dataset.

## Overview

OpenGraph proposes an open-vocabulary hierarchical 3D graph representation for large-scale outdoor environments. It extracts instances and captions from images, maps them incrementally to 3D using LiDAR, and segments based on lane graphs. The system supports zero-shot learning for open‑set classes, enabling recognition of arbitrary object categories not seen during training.

## Methodology

1. **Instance and caption extraction** – Visual images are processed using VLMs to extract object instances and generate descriptive captions, enabling open-set recognition.
2. **Image‑to‑LiDAR projection and 3D incremental mapping** – Extracted instances and captions are projected onto [[LiDAR point clouds]] ⚠️ to obtain geometric grounding. Features are accumulated over time to build persistent 3D object representations.
3. **Lane graph connectivity segmentation** – The environment is segmented based on lane graph structure, yielding a hierarchical graph that organizes objects for navigation and planning.

## Validation

OpenGraph was evaluated on the [[SemanticKITTI]] dataset, achieving the highest segmentation and query accuracy among comparable open‑vocabulary methods. It acts as a benchmark for future open‑vocabulary outdoor mapping algorithms.

## Capabilities

- **Open‑vocabulary mapping with zero‑shot learning** – recognizes object classes never seen during training.
- **3D incremental object‑centric mapping with feature embedding** – builds persistent object representations over time.
- **Hierarchical graph construction based on lane graph connectivity** – organizes objects into a structured graph suitable for navigation and planning.
- **High segmentation and query accuracy in outdoor scenes** – demonstrated on SemanticKITTI.

## Parameters

- **Type**: Open-vocabulary hierarchical 3D graph representation
- **Scale**: Large-scale outdoor environments
- **Input modalities**: Visual images, LiDAR point clouds
- **Output**: Hierarchical graph with instance captions and lane connectivity
- **Validation dataset**: SemanticKITTI

## Relationships

OpenGraph **uses** [[Visual-Language Models (VLMs)]] for image‑text reasoning, [[LiDAR]] for geometric grounding, and lane graph connectivity for structural segmentation. It **implements** incremental 3D object‑centric mapping and open‑vocabulary segmentation. The algorithm **depends on** several processing steps: instance extraction from images, caption generation, and projection onto point clouds. For real‑time deployment it **depends on** [[ROS2]] and typical autonomous driving sensor stacks (implied by its outdoor application).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `OpenGraph` --[[uses]] ⚠️ ⚠️--> `Visual-Language Models (VLMs)`
- `OpenGraph` --[[uses]] ⚠️ ⚠️--> `LiDAR`
- `OpenGraph` --[[depends_on]] ⚠️--> `SemanticKITTI`