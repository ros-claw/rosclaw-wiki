---
id: topometric_navigation
title: Topometric Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:40:38'
last_reinforced: '2026-04-29T21:40:38'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Topometric Navigation

## Overview

**Topometric navigation** is a hybrid approach that combines topological (graph-based) and metric (geometric) representations for robot navigation. It integrates global topological path planning with local metric control, enabling long-horizon navigation without requiring globally consistent metric maps. This balance allows agents to plan efficiently over large environments while maintaining the precision needed for obstacle avoidance and fine-grained manipulation.

Topometric maps typically consist of a topological graph whose nodes represent key locations or regions, each of which may contain a local metric submap. Transitions between nodes are guided by the topological structure, while within each node, metric methods handle precise motion.

## Capabilities

- **Balances global planning efficiency with local accuracy** – Topological planning reduces the search space to a graph, while metric control ensures precise execution near obstacles and goals.
- **Enables longer horizons than pure metric maps** – Pure metric SLAM and planning degrade over large scales due to drift and computational cost; topometric methods scale by leveraging topological abstraction.
- **Robust to partial metric inconsistency** – Because the global map is topological, small metric errors do not propagate catastrophically.

## Relationship to Other Concepts

- Used by: [[TANGO]] – the paper introducing TANGO (from `papers/2509.08699.pdf`) employs topometric navigation as a core component.
- Depends on: [[Topological Navigation]] ⚠️, [[Metric Navigation]] ⚠️ – since it combines both paradigms.
- Implements: [[Long-Horizon Navigation]] ⚠️ – enabling robots to navigate over hundreds of meters or more without global metric maps.
- Related to: [[Navigation Planning]] ⚠️, [[Map Representation]] ⚠️, [[SLAM]] – topometric maps can be built using a hybrid SLAM approach that maintains both graph structure and local metrics.

## How It Works

A typical topometric navigation system:

1. Builds a topological graph from visual or spatial landmarks (e.g., keyframes, place recognition).
2. Associates each node with a local metric map (e.g., occupancy grid, point cloud) or a learned policy.
3. Plans a path over the topological graph (e.g., using Dijkstra or A* on node connectivity).
4. Executes the plan by switching between metric controllers for traversing each edge or node region.
5. Handles loop closures by updating topology, not by globally rectifying metric geometry.

## Advantages Over Pure Approaches

| Aspect | Metric-Only | Topological-Only | Topometric |
|--------|-------------|------------------|------------|
| Global consistency | Required | Not required | Not required |
| Local accuracy | High | Low | High |
| Planning complexity | O(m²) | O(n²) with n ≪ m | O(n² + local cost) |
| Robustness to drift | Poor | Good | Good |
| Scalability | Poor for large environments | Good | Good |

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Topometric Navigation` --[[related_to]] ⚠️--> `TANGO` _(wikilink)_
