---
id: room_to_room_benchmark
title: Room-to-Room Benchmark
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:43:39'
last_reinforced: '2026-04-30T02:43:39'
supersedes: []
sources:
- papers/2002.10638.pdf
source_type: arxiv_paper
---

## Room-to-Room Benchmark (R2R)

The **Room-to-Room Benchmark (R2R)** is a standard evaluation framework for Vision-and-Language Navigation (VLN) agents. It consists of indoor navigation instructions paired with ground-truth trajectories derived from photo-realistic 3D scans of real buildings. The benchmark is widely used to assess an agent’s ability to follow natural language commands in unseen environments.

### Overview

The R2R benchmark was introduced to provide a reproducible and challenging testbed for VLN research. It uses high-fidelity visual inputs from the Matterport3D ⚠️ ⚠️ ⚠️ dataset and requires agents to navigate from a starting location to a target room, following step-by-step instructions. The benchmark measures both the accuracy of reaching the goal and the efficiency of the chosen path.

### Parameters

- **Type**: Navigation benchmark for VLN agents.
- **Environments**: Indoor rooms from photo-realistic 3D scans (Matterport3D ⚠️ ⚠️ ⚠️).
- **Primary Metric**: Success rate weighted by path length (SPL). This metric combines task completion (success) with path efficiency, penalizing agents that reach the goal via overly long routes.
- **Previous State-of-the-Art SPL**: 47%
- **New State-of-the-Art SPL Achieved**: 51% (by Prevalent, as reported in the source paper)

### Capabilities

- Standard evaluation for VLN agents, allowing direct comparison across models.
- Measures both success (reaching the target) and path efficiency, incentivizing agents that follow instructions concisely.
- Supports multi-step instructions and requires grounding language to visual observations.
- Includes both training and test splits with unseen environments to test generalization.

### Relationships

- **Used to evaluate**: Prevalent, VLN-BERT, Speaker-Follower, and many other VLN agents.
- **Part of**: The broader Embodied AI evaluation ecosystem, alongside benchmarks like RoboTHOR ⚠️ and Habitat.
- **Depends on**: Matterport3D ⚠️ ⚠️ ⚠️ for visual rendering and ground-truth trajectories.
- **Used by**: The VLN ⚠️ research community to benchmark progress in instruction-following navigation.

### References

- Source paper: *“Prevalent: A Pre-trained Visual-Language Model for Vision-and-Language Navigation”* (arXiv:2002.10638)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room-to-Room Benchmark` --related_to ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `Room-to-Room Benchmark` --depends_on ⚠️--> `Prevalent`
- `Room-to-Room Benchmark` --related_to ⚠️ ⚠️--> `Embodied AI`
