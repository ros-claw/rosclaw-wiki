---
id: continuous_action_space
title: Continuous Action Space
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:38:44'
last_reinforced: '2026-04-30T02:38:44'
supersedes: []
sources:
- papers/2104.10674.pdf
source_type: arxiv_paper
---

## Continuous Action Space

**Continuous Action Space** is a framework in reinforcement learning and embodied AI where the agent selects actions from a continuous range of values (e.g., velocities, joint torques) rather than from a discrete set of predefined movements. This enables fine-grained control and more realistic robotic navigation, but introduces additional challenges such as obstacle avoidance and longer planning horizons.

### Relationship to Discrete Action Space

Continuous Action Space [[contrasts_with::Discrete Action Space]] ⚠️. In discrete action spaces, the agent chooses from a small set of commands (e.g., "move forward 1 meter", "turn left 90°"). Continuous spaces allow arbitrary movement parameters (e.g., "linear velocity 0.73 m/s, angular velocity 0.15 rad/s"), which mirrors real-world robot control more closely but increases the difficulty of policy learning and collision avoidance.

### Applications

- Used by the [[Hierarchical Cross-Modal (HCM) Agent]] for vision-and-language navigation tasks.
- Employed in the [[Robo-VLN]] system to achieve smoother and more flexible trajectory generation.

### Challenges

The shift from discrete to continuous actions introduces:

- **Obstacle Avoidance**: Agents must avoid collisions while following continuous trajectories, requiring higher‑fidelity perception and control.
- **Longer Planning Horizons**: The combinatorial space of possible action sequences grows dramatically, making reward shaping and exploration more complex.
- **Safety Constraints**: Continuous commands must be bounded and smoothed to prevent mechanical damage or erratic behavior.