---
id: occupancy_based_representation
title: Occupancy-based representation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:50:06'
last_reinforced: '2026-04-29T21:50:06'
supersedes: []
sources:
- papers/2507.20217.pdf
source_type: arxiv_paper
---

## Occupancy-based Representation

### Overview

An **occupancy-based representation** encodes both occupancy status (occupied vs. free space) and semantic labels in a structured grid format, providing a dense, interpretable model of the environment. It is particularly well-suited for humanoid robot perception, where rich 3D geometric understanding combined with semantic meaning is critical for safe and effective interaction.

### Capabilities

- Provides rich semantic and 3D geometric information of the surrounding environment.
- Suitable for Humanoid Occupancy perception tasks, enabling robust scene understanding.
- Integrates occupancy status with object-level semantics to support higher-level reasoning.

### Relationships

- **Used by**: Humanoid Occupancy — the representation serves as the core perceptual backbone for humanoid robots to model their surroundings.
- **Related to**:
  - Task planning ⚠️ — semantic occupancy grids facilitate object-aware task decomposition and manipulation.
  - Navigation ⚠️ — occupancy information directly supports path planning and obstacle avoidance in 3D space.

### Description

Occupancy-based representation encodes both occupancy status and semantic labels in a grid format, offering comprehensive environmental understanding. By discretizing the world into volumetric cells, each cell carries a probability of occupancy and, where applicable, a semantic class (e.g., "table", "wall", "person"). This dual-channel representation bridges low-level geometric sensing with high-level reasoning, making it a natural fit for humanoid robots that must operate in cluttered, human-centric environments. The representation is derived from sensor data (e.g., depth cameras, LiDAR) and can be updated incrementally, supporting dynamic scene changes.

### Source

This concept is extracted from the arxiv paper `papers/2507.20217.pdf`.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Occupancy-based representation` --related_to ⚠️--> `Humanoid Occupancy` _(wikilink)_
