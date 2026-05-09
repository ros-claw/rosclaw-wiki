---
id: dd_ppo_based_local_controller
title: DD-PPO-based local controller
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:30:40'
last_reinforced: '2026-04-30T01:30:40'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

# DD-PPO-based Local Controller

The **DD-PPO-based local controller** is a reinforcement learning algorithm that predicts low-level motor commands for robotic navigation. It forms part of the _Vision and Language Navigation in the Real World via Online Visual Language Mapping_ system, handling the translation of high‑level waypoints into executable actions.

## Overview

This controller implements [[DD-PPO]] ⚠️ ⚠️ ⚠️ (Decentralized Distributed Proximal Policy Optimization), a scalable on‑policy RL algorithm. It processes the current observation (e.g., depth image, odometry) and a local target waypoint, then outputs direct action commands (e.g., linear and angular velocities) to steer the robot toward that waypoint. The controller operates in real‑time as the lowest‑level motion planner, bridging the gap between a global navigation plan and raw motor output.

## Parameters

| Field | Value |
|-------|-------|
| **Algorithm base** | [[DD-PPO]] ⚠️ ⚠️ ⚠️ (Decentralized Distributed Proximal Policy Optimization) |
| **Input** | Current observation (sensor data) + waypoint (target pose relative to robot) |
| **Output** | Action command (e.g., velocity commands, joint torques) |

## Capabilities

- Predicts low‑level actions for local navigation in real‑time.
- Executes local motion planning by mapping waypoints to control signals.
- Generalizes across environments through reinforcement learning from interaction.

## Relationships

> _These connections are maintained in the wiki for traceability._

- **part_of** → [[Vision and Language Navigation in the Real World via Online Visual Language Mapping]] ⚠️ – The controller is a core component of that overall navigation system.
- **depends_on** → [[DD-PPO]] ⚠️ ⚠️ ⚠️ – The training and inference are built upon the DD-PPO algorithm.

## Context & Usage

The DD-PPO-based local controller is typically deployed after a higher‑level planner has generated a sequence of waypoints. By taking the current observation and the next waypoint, it produces continuous action commands at a high frequency. This design decouples high‑level reasoning (e.g., visual‑language grounding) from low‑level control, enabling the system to leverage RL trained in simulation or real‑world data.

The controller’s parameters can be fine‑tuned via domain randomization or sim‑to‑real transfer. It is designed to work with a variety of wheeled or legged platforms, provided the input observation space and action space are matched during training.