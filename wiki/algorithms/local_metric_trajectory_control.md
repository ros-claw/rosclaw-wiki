---
id: local_metric_trajectory_control
title: Local Metric Trajectory Control
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:37:42'
last_reinforced: '2026-04-29T21:37:42'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Local Metric Trajectory Control

**Local Metric Trajectory Control** is an algorithm within the [[TANGO]] framework that computes continuous local trajectories for a robot based on monocular depth and traversability estimates. Its primary inputs are [[Monocular Depth and Traversability Estimation]] outputs, which it uses to generate smooth, collision-free paths in real-time.

## Overview

The algorithm operates as a closed-loop controller that reconciles a local metric map with high-level navigation commands. By interpreting traversability scores and depth measurements, it predicts a sequence of feasible poses while avoiding obstacles. This enables continuous local trajectory prediction and obstacle avoidance without relying on global path pre-computation.

## Capabilities

- **Continuous local trajectory prediction**: Generates a dense sequence of waypoints at high frequency, ensuring smooth motion.
- **Obstacle avoidance**: Integrates obstacle geometry from depth estimates to dynamically adjust trajectories.

## Input & Output

- **Input**: Monocular depth and traversability estimates (see [[Monocular Depth and Traversability Estimation]]).
- **Output**: A set of control commands (e.g., linear/angular velocities) or pose sequences that the robot can execute.

## Role in [[TANGO]]

Local Metric Trajectory Control is a core component of TANGO’s control pipeline. It bridges perception and action by translating learned terrain understanding into executable motion. It depends on accurate depth estimation and traversability scoring, and its output is sent to low-level motor controllers or a [[ROS2 Navigation Stack]] ⚠️ node.

## Relationships

- **part_of** [[TANGO]]
- **uses** [[Monocular Depth and Traversability Estimation]]

## Implementation Notes

The algorithm is designed for real-time execution on edge hardware (e.g., NVIDIA Jetson). It can be integrated as a ROS2 node that subscribes to `/depth` and `/traversability` topics and publishes `/cmd_vel` or trajectories. Reference implementation details are available in the corresponding arXiv paper `2509.08699.pdf`.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Local Metric Trajectory Control` --[[extends]] ⚠️--> `TANGO`
