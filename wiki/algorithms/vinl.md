---
id: vinl
title: ViNL
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:43:31'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# ViNL

**ViNL** (Visual Navigation and Locomotion) is a fully learned, model-free approach for quadrupedal robots that combines separate [[Visual Navigation Policy]] and [[Visual Locomotion Policy]] ⚠️ ⚠️ networks to navigate unknown indoor environments while stepping over small obstacles. It achieves zero-shot [[Sim-to-Real]] ⚠️ transfer without requiring co-training of the two policies.

## Overview

ViNL is designed to enable [[Quadrupedal Robots]] ⚠️ (e.g., [[Unitree Go1]] ⚠️, [[Spot Robot]] ⚠️) to traverse unseen apartments and similar indoor spaces, stepping over obstacles such as shoes, toys, and cables **without disrupting them**. The system takes as input **egocentric vision** and outputs linear and angular velocity commands that are then translated into joint-level control actions. ViNL is a **model-free** system — it requires no explicit obstacle maps, privileged terrain information, or pre-built environment models.

## System Architecture

ViNL consists of two independently trained neural network policies:

- **Visual Navigation Policy**: processes egocentric visual input to produce velocity commands (linear and angular velocities). This policy is responsible for steering the robot toward a distant goal while avoiding large obstacles.
- **Visual Locomotion Policy**: converts those velocity commands into joint-level actions, controlling the robot's legs to step over small obstacles (e.g., shoes, toys, cables) while maintaining stability.

The two policies are trained in **different simulators** and are never co-trained; instead, the navigation velocity commands are fed directly into the locomotion policy at deployment time (zero-shot transfer). This decoupled architecture simplifies training and allows each policy to specialize.

## Training Methodology

Both policies are trained **end-to-end** using deep reinforcement learning, each in its own simulator environment. The navigation policy learns to reach distant goals from visual observations, while the locomotion policy learns to follow velocity commands while stepping over small obstacles. No co-training is required — the navigation policy's output (velocity commands) is treated as a fixed input to the locomotion policy during deployment, enabling zero-shot sim-to-real transfer without any fine-tuning or joint optimization.

## Capabilities

- Navigate to distant goals in unknown indoor environments.
- Step over small obstacles (shoes, toys, cables) without disrupting them.
- Output linear and angular velocity commands from egocentric vision.
- Control robot joints to avoid stepping on obstacles while following commands.
- Achieve zero-shot sim-to-real transfer without co-training.

## Performance

- **Success improvement**: +32.8% over prior methods that relied on privileged terrain maps.
- **Collision reduction**: -4.42 collisions per meter compared to baseline approaches.

## Relationships

- **[[uses]] ⚠️**: [[Visual Navigation Policy]], [[Visual Locomotion Policy]] ⚠️ ⚠️
- **[[implements]] ⚠️**: model-free visual navigation, model-free visual locomotion
- **[[depends_on]] ⚠️**: Two different simulators (without co-training)
- **[[supersedes]] ⚠️**: Prior work on robust locomotion using privileged terrain maps (outperforms by +32.8% success, -4.42 collisions per meter)

## Further Reading

- Paper: *ViNL: Visual Navigation and Locomotion Over Obstacles* (arXiv:2210.14791)
- Related: [[Legged Locomotion]] ⚠️, [[Deep Reinforcement Learning]] ⚠️, [[Obstacle Avoidance]] ⚠️