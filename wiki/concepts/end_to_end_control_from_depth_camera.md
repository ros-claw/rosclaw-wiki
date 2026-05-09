---
id: end_to_end_control_from_depth_camera
title: End-to-end control from depth camera
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:28:47'
last_reinforced: '2026-04-30T04:28:47'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

## Overview

**End-to-end control from depth camera** is a learning-based approach that maps raw depth image data directly to motor commands, bypassing the hand-crafted perception, state estimation, and control layers of classical robotics pipelines. By training a single neural network policy — typically via [[Deep Reinforcement Learning]] ⚠️ ⚠️ — this paradigm can handle noisy, high-dimensional sensor streams and produce robust locomotion behaviors without requiring precise engineered models.

## Motivation

Classical approaches require independently engineering perception, actuation, and control systems to very low tolerances. Each subsystem must be calibrated, tuned, and validated, making deployment in novel environments brittle. End-to-end learning avoids this by training a single policy from raw camera data to motor commands, allowing the system to discover its own internal representations and directly optimize for task outcomes.

## Capabilities

- Bypasses modular perception and control pipelines, reducing engineering overhead and the need for hand-tuned intermediate representations.
- Handles imprecise or noisy sensor data directly, leveraging the policy's learned robustness rather than requiring precise filtering or state estimation.

## Specifications

| Parameter | Value |
|---|---|
| Sensor | Single front-facing [[Depth Camera]] ⚠️ |
| Output | Control commands (e.g., joint torques or velocities) |
| Learning paradigm | [[Deep Reinforcement Learning]] ⚠️ ⚠️ (DRL) |
| Example application | [[Extreme Parkour Policy]] (see [[#Relationships]] ⚠️) |

## Relationships

- **Part of** → [[Extreme Parkour Policy]] — the end-to-end depth-to-control policy forms the core learning component of the larger parkour system.
- **Contrasts with** → [[Classical modular perception-actuation-control systems]] ⚠️, which decompose the problem into separate modules (e.g., visual odometry, mapping, trajectory optimization, low-level control).

## References

- arXiv 2309.14341 – *Extreme Parkour Policy* (source paper for this concept).