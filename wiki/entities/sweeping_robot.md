---
id: sweeping_robot
title: Sweeping Robot
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:53:44'
last_reinforced: '2026-04-30T02:53:44'
supersedes: []
sources:
- papers/2602.18424.pdf
source_type: arxiv_paper
---

## Sweeping Robot

A **Sweeping Robot** is a wheeled mobile robot designed for cleaning flat surfaces such as floors, typically in indoor environments. It is characterized by its inability to traverse stairs or uneven terrain, confining its operation to level ground.

### Overview

Sweeping robots are a common type of domestic or commercial service robot. They rely on wheeled mobility ⚠️ for locomotion and often integrate sensors (e.g., bumpers, LiDAR, cameras) for navigation. Due to their wheeled design, they are limited to flat, obstacle-free surfaces and cannot handle stairs, thresholds, or steep inclines.

### Capabilities

- **Mobility type**: wheeled ⚠️
- **Can traverse stairs**: false  
- **Operating domain**: limited to flat surfaces  
- **Primary task**: floor sweeping / cleaning

Because they cannot ascend or descend stairs, sweeping robots are typically deployed on a single floor level. Their navigation systems often assume a flat continuous environment, making them unsuitable for multi-story buildings without manual intervention.

### Relationships

- **Example in**: Capability-Conditioned Navigation (CapNav) – The sweeping robot is used as one of several robot types in the CapNav framework to demonstrate how navigation policies can be conditioned on the robot’s physical capabilities. It serves as a contrast to robots that can traverse stairs, such as legged robots.
- **Depends on**: Flat Surface Navigation ⚠️ – The robot’s control algorithms must assume a planar operating environment.
- **Related to**: Domestic Service Robots ⚠️, Floor Cleaning Robots ⚠️, Wheeled Locomotion ⚠️