---
id: extreme_parkour_robot
title: Extreme Parkour Robot
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T04:16:42'
last_reinforced: '2026-04-30T04:16:42'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# Extreme Parkour Robot

The **Extreme Parkour Robot** is a small, low-cost legged robot designed to perform advanced parkour maneuvers such as high jumps, long jumps, handstands, and running across tilted ramps. Despite its imprecise actuation and minimal sensing, it demonstrates surprising agility and generalization to novel obstacle courses. The robot was introduced in the paper “Extreme Parkour with Legged Robots” (arXiv:2309.14341).

## Hardware Description

The robot is built around a small, low-cost platform with the following key characteristics:
- **Size**: Small (dimensions not specified, but implied to be compact).
- **Cost**: Low, making it accessible for research and experimentation.
- **Actuation**: Imprecise—the robot does not rely on high-precision motors or joint encoders.
- **Sensor**: A single Front-facing Depth Camera ⚠️ ⚠️ that is low-frequency, jittery, and prone to artifacts. This limited perception challenges the control system to operate under severe sensor noise.

The minimal hardware design deliberately reduces cost and complexity, pushing the control policy to handle real-world imperfections.

## Demonstrated Performances

The robot has been shown to reliably execute the following maneuvers:

- **High jump** onto obstacles up to **2× its own height**.
- **Long jump** across gaps up to **2× its own body length**.
- **Handstand** – balancing on its front legs.
- **Running** across tilted ramps.
- **Generalization** to novel obstacle courses with different physical properties (e.g., varying friction, surface textures, and obstacle geometries).

These capabilities are achieved without task-specific engineering; a single learned policy handles all behaviors.

## Relationships

- **uses** → Front-facing Depth Camera ⚠️ ⚠️ for perception.
- **uses** → Extreme Parkour Policy – a reinforcement-learning-based controller that handles the low-quality sensor data and imprecise actuation.
- **depends_on** → Imprecise actuation and low-cost hardware (from design choices).
- **part_of** → Research in embodied AI and sim-to-real transfer for agile locomotion.

## Significance

The Extreme Parkour Robot demonstrates that impressive locomotion skills can be achieved with inexpensive hardware and a single, robust policy, reducing the gap between simulation and real-world performance. Its success highlights the potential of learning-based approaches to compensate for sensor and actuator limitations.

## References

- *Extreme Parkour with Legged Robots* – arXiv:2309.14341 (2023). Describes the robot design, control policy, and experimental results.