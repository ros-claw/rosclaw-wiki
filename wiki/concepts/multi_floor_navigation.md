---
id: multi_floor_navigation
title: Multi-floor Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:01:56'
last_reinforced: '2026-04-30T00:01:56'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

### Multi-floor Navigation

**Multi-floor Navigation** refers to the ability of a robot or agent to plan and execute movement across multiple levels of a building or structure, including transitions between floors (e.g., via stairs, ramps, or elevators). It is a specialized subfield of [[Navigation]] ⚠️ that introduces vertical spatial reasoning as a core requirement, moving beyond planar assumptions.

#### Capabilities

- **Handles cross-floor transitions**: The system can identify and traverse vertical connection points (stairs, elevators, ramps) to move from one floor to another while maintaining global consistency of the environment model.
- **Vertical spatial reasoning**: The planner incorporates height and floor-level information into its state space, enabling decisions such as which floor a destination lies on and the most efficient vertical route.

#### Challenges

- **Single-floor assumption**: Most conventional navigation stacks (e.g., [[ROS Navigation Stack]] ⚠️, [[MoveIt2]] ⚠️) assume a flat, single-floor environment, and do not natively support z-axis planning or floor transitions.
- **Requirement for offline maps**: Many current approaches rely on pre‑built [[3D Map Representation]] ⚠️ or floor-plan overlays; dynamically constructing multi-floor maps online remains an open problem, particularly in unknown or unstructured environments.

#### Relationships

- **Implements**: [[Vertical Spatial Reasoning]] ⚠️
- **Depends on**: [[3D Semantic Mapping]] ⚠️, [[Multi-Level Path Planning]] ⚠️
- **Challenged by**: [[Single-Floor Assumption]] ⚠️, [[Offline Map Requirement]] ⚠️
- **Part of**: [[Embodied Indoor Navigation]] ⚠️

The source paper (arxiv:2505.23019) proposes a method to overcome the offline-map dependency by learning a latent representation that generalizes across floors without explicit map pre‑construction.