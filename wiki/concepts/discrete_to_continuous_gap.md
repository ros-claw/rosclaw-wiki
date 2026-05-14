---
id: discrete_to_continuous_gap
title: Discrete-to-Continuous Gap
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:21:20'
last_reinforced: '2026-04-30T02:21:20'
supersedes: []
sources:
- papers/2203.02764.pdf
source_type: arxiv_paper
---

## Discrete-to-Continuous Gap

The **Discrete-to-Continuous Gap** is a fundamental challenge in robot navigation that arises from the mismatch between **Discrete Environments ⚠️ ⚠️** (e.g., topological graphs, navigation meshes) and **Continuous Environments ⚠️ ⚠️** (e.g., physical spaces with continuous states and low-level dynamics). The gap represents the difficulty of translating high-level, discrete actions into low-level, continuous controls that can be executed on real hardware.

In a discrete navigation setup, an agent operates on a finite set of states (nodes) and actions (edges), often relying on a known connectivity graph to plan paths. The agent's "decision space" is abstracted to **node-to-node** movement, grounded in navigable images or high-level commands. However, real-world robots must function in a continuous state space, requiring smooth, fine-grained control over actuators and sensors. The discrete-to-continuous gap is the barrier between these two representations.

### Description

The gap originates from the **discrete assumption** that the agent has prior knowledge of the connectivity graph and can execute high-level actions (e.g., "move to waypoint B") without concerning itself with the exact trajectory or actuator commands. In contrast, **continuous navigation** demands that the robot generate a stream of low-level commands (e.g., velocities, joint torques) that respect kinematics, dynamics, and environmental constraints. The gap is addressed by **generating candidate waypoints**—intermediate goals that bridge the discrete plan to a continuous control policy, effectively sampling the continuous space into tractable discrete subproblems.

### Parameters

| Parameter | Description |
|-----------|-------------|
| `discrete_assumption` | Prior knowledge of the connectivity graph (i.e., known topological structure). |
| `continuous_requirement` | Necessity for low-level controls (e.g., motor commands, PID setpoints) to execute a plan. |

### Relationships

- **Depends on:** Discrete Environments ⚠️ ⚠️, Continuous Environments ⚠️ ⚠️.
- **Addressed by:** generating candidate waypoints that transform high-level decisions into low-level motion primitives.
- **Related to:** Topological Navigation ⚠️, Hierarchical Planning, Sim-to-Real Transfer (where the gap also manifests in abstraction mismatches).

### See Also

- Discrete vs Continuous Control ⚠️
- Graph-based Planning ⚠️
- Low-level Policy ⚠️