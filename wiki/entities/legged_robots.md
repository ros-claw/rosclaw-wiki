---
id: legged_robots
title: Legged Robots
type: entity
tags: []
confidence: 0.9
created_at: '2026-04-29T20:55:07'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.20739.pdf
- papers/2505.19214.pdf
- papers/2512.09537.pdf
source_type: arxiv_paper
---

# Legged Robots

Legged robots are a class of mobile robots that use articulated limbs—typically two (**bipeds**), four (**quadrupeds**), or six (**hexapods**)—for locomotion. They are capable of traversing terrain that is inaccessible to wheeled or tracked robots, such as stairs, rubble, and uneven natural surfaces. In the context of embodied AI and semantic exploration, legged robots serve as the physical platform for deploying perception, planning, and control algorithms.

## Overview

The generic legged locomotion platform referenced in [[Decision-Driven Semantic Object Exploration (DD-SOE)]] is not a specific commercial or research model but rather a general class of quadrupedal or bipedal systems used to validate the DD-SOE approach. This platform type, often described as a **generic legged locomotion platform**, abstracts away hardware-specific details to emphasize algorithm generality. Both simulation experiments (e.g., in MuJoCo, Isaac Gym) and real-world deployments on platforms such as [[Unitree Go1]] ⚠️, [[ANYmal]], or bipedal humanoids have demonstrated the method's effectiveness.

## Capabilities

Legged robots offer a wide range of capabilities that make them ideal for unstructured environments:

- **Navigate in complex environments** — legged robots can step over obstacles, climb slopes, and traverse debris, making them suited for unstructured indoor/outdoor spaces.
- **Agile locomotion in complex 3D environments** — dynamic gaits (trot, pace, bound) allow high-speed maneuvers over uneven terrain while maintaining stability.
- **Omnidirectional obstacle avoidance** — ability to move in any direction and quickly adapt motion plans to avoid collisions without stopping or reorienting.
- **Perform semantic object exploration** — equipped with onboard sensors, they actively seek and recognize objects of interest using decision-driven exploration policies (see [[semantic exploration]] ⚠️).
- **Reactive navigation** — legged robots can run [[REASAN]] (a reactive navigation system) for real-time path adaptation in dynamic environments, leveraging leg-based agility to respond to sudden obstacles or changes in terrain.

### Sensing and Perception

Legged robots rely on a combination of sensors for perception and navigation. Common onboard sensors include [[LiDAR]] for precise depth sensing and RGB-D cameras for visual-semantic understanding. The [[Omni-Perception]] system provides a unified framework for combining these modalities, enabling robust localization, mapping, and object detection during exploration.

## Relationship with DD-SOE and REASAN

Legged robots **use** the [[Decision-Driven Semantic Object Exploration (DD-SOE)]] algorithm to guide their exploration behavior. DD-SOE provides a sequential decision-making framework that balances semantic information gain, localization cost, and safety, enabling the robot to efficiently discover specified object categories without prior map knowledge. The perception backbone for DD-SOE often incorporates [[Omni-Perception]] to process multi-modal sensor data and fuse semantic information with geometric maps.

In addition to high-level semantic exploration, legged robots **use** [[REASAN]] for reactive navigation. REASAN provides a low-level reactive control layer that handles instantaneous obstacle avoidance and terrain adaptation, complementing the deliberative planning of DD-SOE. This combination of semantic reasoning and reactive agility is especially powerful in cluttered or unpredictable environments.

## See Also

- [[Locomotion Controllers]] ⚠️ — low-level gait generation
- [[Sim-to-Real Transfer]] — necessary for deploying simulation-trained policies on physical legged robots
- [[Semantic Mapping]] ⚠️ — the underlying representation fused during exploration
- [[Omni-Perception]] — perception framework used by legged robots in semantic exploration
- [[REASAN]] — reactive navigation system for legged platforms

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Legged Robots` --[[uses]] ⚠️ ⚠️ ⚠️--> `Decision-Driven Semantic Object Exploration (DD-SOE)`
- `Legged Robots` --[[uses]] ⚠️ ⚠️ ⚠️--> `REASAN`
- `Legged Robots` --[[depends_on]] ⚠️ ⚠️--> `ANYmal`
- `Legged Robots` --[[depends_on]] ⚠️ ⚠️--> `LiDAR`
- `Legged Robots` --[[uses]] ⚠️ ⚠️ ⚠️--> `Omni-Perception`