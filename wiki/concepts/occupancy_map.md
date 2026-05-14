---
id: occupancy_map
title: Occupancy map
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:31:20'
last_reinforced: '2026-04-30T04:31:20'
supersedes: []
sources:
- papers/2312.03275.pdf
source_type: arxiv_paper
---

# Occupancy Map

An **occupancy map** is a grid-based representation of the environment where each cell stores the probability of being occupied, free, or unknown. In embodied AI and robotics, occupancy maps are built incrementally from sensor data, such as depth images, and serve as a spatial memory for navigation, mapping, and exploration.

## Description

An occupancy map divides the environment into grid cells indicating occupancy probability, built from depth observations in VLFM.

## Capabilities

- **Represent free and occupied space** from depth data — each cell's occupancy probability is updated using a sensor model as the robot moves.
- **Identify frontiers for exploration** — cells at the boundary between known free space and unknown space are flagged as frontier cells, guiding the robot toward unexplored areas.

## Relationships

- **Used by**: VLFM — the occupancy map is a core component that provides a metric map of the environment for frontier-based exploration and navigation.