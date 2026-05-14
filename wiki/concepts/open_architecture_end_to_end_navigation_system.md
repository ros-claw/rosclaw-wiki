---
id: open_architecture_end_to_end_navigation_system
title: Open-Architecture End-to-End Navigation System
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:09:13'
last_reinforced: '2026-04-30T01:09:13'
supersedes: []
sources:
- papers/2410.06239.pdf
source_type: arxiv_paper
---

# Open-Architecture End-to-End Navigation System

An **Open-Architecture End-to-End Navigation System** is a lightweight, modular, real-time framework for autonomous navigation that integrates multiple components into an end-to-end pipeline. Designed for open‑vocabulary, zero‑shot deployment, the system is built on ROS2 and combines an LLM-based Planner with Hierarchical Scene Graph Construction to enable robust navigation in unseen environments.

## Overview

The system fuses onboard sensory data for localization and mapping with open‑vocabulary semantics to build hierarchical scene graphs from a continuously updated semantic object map. An LLM-based Planner uses these graphs to generate and adapt goal‑oriented plans in real time. This architecture allows the robot to navigate zero‑shot with a task success rate exceeding 88%.

## Capabilities

- **Zero‑shot real‑world autonomous navigation** – no prior training on the target environment required.
- **Task success rate > 88%** across diverse indoor/outdoor scenarios.

## System Components

The system depends on three tightly integrated modules:

- **ROS2** – provides the communication backbone, sensor fusion, and hardware abstraction layer.
- **Hierarchical Scene Graph Construction** – continuously builds and updates a multi‑level semantic representation of the environment from raw sensor data.
- **LLM-based Planner** – receives the hierarchical scene graph and a high‑level goal, then generates and refines action sequences in a closed‑loop manner.

## Deployment

The system has been deployed on the Unitree Go2 quadruped robot, where it demonstrated robust real‑time performance and adaptability to dynamic obstacles and novel object categories.

## Key Relationships

- Uses ROS2 as its middleware.
- Depends on Hierarchical Scene Graph Construction for world modeling.
- Implements end‑to‑end control via LLM-based Planner.
- Deployed on Unitree Go2 (hardware platform).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Open-Architecture End-to-End Navigation System` --applies_to ⚠️--> `Unitree Go2`
