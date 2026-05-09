---
id: habitat
title: Habitat
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-30T00:20:17'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.17221.pdf
- code/PKU-SEC-Lab_EfficientNav/README.md
source_type: arxiv_paper
---

# Habitat

**Habitat** is a 3D simulation platform designed for embodied AI research. It enables the construction of photorealistic, physically grounded simulated environments in which agents can be trained and evaluated on tasks such as navigation, manipulation, and instruction following. Habitat supports rapid rendering, flexible sensor suites, and modular agent control interfaces, making it a foundational tool for sim-to-real transfer in robotics.

## Capabilities

- **Environment Construction**: Habitat provides APIs to load 3D scans of real-world spaces (e.g., Matterport3D, Gibson, Replica) and populate them with interactive objects and agents.
- **Physical Simulation**: The platform includes a physics engine that models collisions, gravity, and simple articulation, allowing tasks like object rearrangement and locomotion.
- **Sensor Simulation**: Supports RGB, depth, semantic segmentation, and other sensor modalities with configurable intrinsics and extrinsics.
- **Multi‑Agent Support**: Multiple agents can coexist in the same scene, enabling multi‑agent collaboration or competition scenarios.
- **High Performance**: Optimized rendering and headless mode allow thousands of environment steps per second for large‑scale training.

## Installation

Habitat is distributed as two core components: [[Habitat-Sim]] and [[Habitat-Lab]] ⚠️ ⚠️. Both are installed from source; see the [official repository](https://github.com/facebookresearch/habitat-sim) for build instructions and dependencies.

## Relationships

- [[Habitat]] **depends_on** [[PyTorch]] ⚠️ and [[OpenGL]] ⚠️ for rendering and GPU acceleration.
- [[Habitat]] **used_to_construct** [[VLN-Ego dataset]], a dataset for egocentric vision‑language navigation that pairs photorealistic renderings with natural language instructions.
- [[Habitat]] **used_by** [[VLN-R1]], a reinforcement‑learning architecture for vision‑language navigation tasks.
- [[Habitat]] **used_by** [[EfficientNav]], a navigation policy that leverages the platform for training and evaluation.

## Usage in Embodied AI

The simulator is commonly integrated with learning frameworks such as [[Habitat-Lab]] ⚠️ ⚠️ (for training and evaluation) and [[Habitat-Sim]] (the core simulation engine). Researchers extend Habitat with custom tasks (e.g., ObjectNav, PointNav), and combine it with [[ROS2]] to serve as a testing ground for robot control policies before deployment on physical platforms like [[Unitree G1]] or [[UR5]] ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Habitat` --[[uses]] ⚠️--> `VLN-R1`
- `Habitat` --[[depends_on]] ⚠️--> `Unitree G1`