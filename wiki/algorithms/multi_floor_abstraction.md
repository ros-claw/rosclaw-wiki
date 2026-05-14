---
id: multi_floor_abstraction
title: Multi-Floor Abstraction
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:44:30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

# Multi-Floor Abstraction

The **Multi-Floor Abstraction** module is a hierarchical environment representation algorithm that enables mobile robots to understand and navigate vertical transitions between floors. It dynamically constructs structured models that incorporate stair-aware obstacle mapping and cross-floor topology modeling, allowing the robot to reason about multi-level spaces as part of the ASCENT system.

## Parameters

- **type**: `hierarchical_representation` – the representation decomposes the environment into layers of abstraction, from high-level topology to low-level obstacle geometry.
- **stair_aware**: `true` – the module explicitly models staircases and their geometric constraints, distinguishing them from ramps, elevators, or other vertical connectors.
- **features**:
  - **Stair-aware Obstacle Mapping** – accounts for the unique geometry of staircases (tread depth, riser height, handrail obstacles).
  - **Cross-floor Topology Modeling** – maintains connectivity graphs between floors, including multiple transition points.

## Capabilities

- Dynamically constructs hierarchical floor representations from sensor input (e.g., LiDAR, depth cameras).
- Models transitions between floors by building and maintaining cross-floor topology graphs.
- Stair-aware obstacle mapping that treats staircases as distinct navigable structures.

## Description

The Multi-Floor Abstraction module dynamically builds hierarchical environment representations that include stair-aware obstacle mapping and cross-floor topology modeling, enabling the robot to understand vertical transitions. It processes raw sensor data to create a multi-layered map where low-level occupancy grids on each floor are linked via edge nodes representing staircases or other inter-floor passages. This abstraction layer is crucial for path planning across multiple floors, as it decouples the complexity of intra-floor navigation from inter-floor reasoning.

## Relationships

- **part_of**: ASCENT – this module is a core component of the broader ASCENT architecture, which provides end-to-end autonomous navigation in multi-story buildings.
- **uses**: Hierarchical Representation ⚠️, Obstacle Mapping ⚠️, Topology Modeling ⚠️ – the algorithm relies on these general concepts to produce its output.
- **depends_on**: Stair Detection ⚠️ – accurate stair detection and parameter estimation are prerequisites for stair-aware mapping.
- **implements**: Vertical Transition Planning ⚠️ – by modeling cross-floor topology, the module implements a key capability for multi-floor navigation.

## See Also

- Sim-to-Real Transfer – techniques used to train the abstraction module in simulation before deployment.
- Elevator Navigation ⚠️ – an alternative vertical transition method that may complement the stair-aware approach.

> Based on the ASCENT system described in arXiv:2505.23019.