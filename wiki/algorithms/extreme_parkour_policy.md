---
id: extreme_parkour_policy
title: Extreme Parkour Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:17:39'
last_reinforced: '2026-04-30T04:17:39'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# Extreme Parkour Policy

**Extreme Parkour Policy** is a Single Neural Net Policy ⚠️ trained via Large-scale RL ⚠️ ⚠️ ⚠️ that enables a low-cost robot to perform dynamic parkour maneuvers — including high jumps, long jumps, handstands, and ramp running — by directly mapping a single front-facing depth camera image to precise control commands. The approach demonstrates robust end-to-end control that overcomes imprecise sensing and actuation, and generalizes to novel obstacle courses.

## Overview

The policy operates **end-to-end**: it takes a single depth image from a front-facing camera and outputs motor commands directly, bypassing traditional modular perception and planning systems. This architecture allows the robot to react quickly and precisely despite noisy sensor data and low-frequency actuation.

- **Input**: single front-facing depth camera image
- **Output**: precise control commands
- **Architecture**: monolithic neural network policy
- **Training method**: Large-scale RL ⚠️ ⚠️ ⚠️ entirely in simulation
- **Inference format**: end-to-end (camera → control)

## Learning Approach

The policy is trained entirely in simulation with large-scale reinforcement learning. It uses a single front-facing depth camera as input and outputs control commands directly, bypassing modular perception and planning systems. The reward function is designed to encourage aggressive dynamic maneuvers while maintaining stability and safety during landing.

## Capabilities

- Overcome imprecise sensing and actuation
- Produce highly precise control behavior end-to-end
- Execute high jump, long jump, handstand, and ramp running
- Generalize to novel obstacle courses never seen during training

## Robustness

Despite using a low-cost robot with imprecise actuation and a jittery, low-frequency depth camera, the policy reliably executes precise dynamic maneuvers. The learned policy compensates for sensor noise and actuator delays through massive exposure to domain-randomized simulation environments.

## Related Dependencies

- **depends_on** → Sim-to-real transfer, Large-scale RL ⚠️ ⚠️ ⚠️
- **controls** → Extreme Parkour Robot