---
id: navspace_annotation_pipeline
title: NavSpace Annotation Pipeline
type: skill
tags: []
confidence: 0.95
created_at: '2026-04-30T04:49:01'
last_reinforced: '2026-04-30T04:49:01'
supersedes: []
sources:
- code/TidalHarley_NavSpace/README.md
source_type: official_manual
---

# NavSpace Annotation Pipeline

The **NavSpace Annotation Pipeline** is a skill ⚠️ for extending the NavSpace benchmark by enabling human annotators to collect new trajectory-instruction pairs ⚠️ ⚠️ with spatial language instructions. It provides a web-based interface that integrates Habitat-Sim simulation with manual annotation workflows.

## Purpose

Allows users to extend the benchmark by annotating new trajectories with spatial instructions. This skill is essential for growing the dataset of grounded navigation tasks and for evaluating models on unseen or custom environments.

## Parameters

| Parameter | Value |
|-----------|-------|
| **Implementation** | Flask ⚠️ ⚠️ ⚠️ + Habitat-Sim web UI, using SocketIO ⚠️ ⚠️ ⚠️ for real-time communication |
| **Familiarization gate** | 200 steps (minimum number of environment interaction steps required before annotation) |
| **Output format** | JSON |

## Capabilities

- Collect new trajectory-instruction pairs ⚠️ ⚠️ through a browser interface
- Support for all six subtasks defined in the NavSpace benchmark:
  - Directional instructions
  - Landmark-based instructions
  - Region-based instructions
  - Path-following instructions
  - Object-relative instructions
  - Spatial-relation instructions

## Relationships

- **Uses**: Habitat-Sim, Flask ⚠️ ⚠️ ⚠️, SocketIO ⚠️ ⚠️ ⚠️
- **Part of**: NavSpace benchmark creation ⚠️

The pipeline depends on Habitat-Sim for environment simulation and rendering, Flask ⚠️ ⚠️ ⚠️ for the web server backend, and SocketIO ⚠️ ⚠️ ⚠️ to stream real-time simulation frames and annotation events. It is a core component of the overall NavSpace benchmark toolchain.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `NavSpace Annotation Pipeline` --related_to ⚠️--> `NavSpace benchmark` _(wikilink)_
