---
id: abstract_obstacle_map
title: Abstract Obstacle Map
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:56:06'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.20499.pdf
source_type: arxiv_paper
---

# Abstract Obstacle Map

## Definition

An **Abstract Obstacle Map** is a simplified representation of the environment that highlights obstacle-free regions and reachable areas. It abstracts obstacles to facilitate efficient waypoint generation in continuous environments. By reducing the complexity of the full environment geometry — typically via depth sensors or occupancy grid inputs — it provides a lightweight spatial representation for waypoint prediction without requiring full metric maps.

## Parameters

- **Representation**: compressed/abstracted obstacle layout (e.g., occupancy grid with reduced resolution, convex hulls of obstacles, or free-space approximations).
- **Source**: derived from depth sensors (LiDAR, RGB-D cameras) or an existing [[Occupancy Grid Map]] ⚠️ ⚠️.

## Capabilities

- Represents the environment in a simplified form for waypoint prediction, allowing downstream models to focus on navigable regions without unnecessary granularity.
- Provides a lightweight spatial representation for waypoint prediction, enabling fast and reliable planning for embodied agents operating in real time.
- Simplifies navigation planning by removing sensor noise and retaining only obstacle boundaries or free-space approximations.
- Enables linear reachability checks for local navigation, making it suitable for reactive control policies and real-time decision-making.

## Relationships

- **Used by** [[Abstract Obstacle Map-Based Waypoint Predictor]] — this predictor leverages the abstract map to generate candidate waypoints for local navigation.

## Usage

In a typical navigation pipeline, the Abstract Obstacle Map is constructed from sensor data (e.g., LiDAR or depth cameras) and provides a compact representation that retains only obstacle boundaries or free-space approximations. This map is then queried by the waypoint predictor to determine which directions are traversable and to compute waypoints that avoid obstacles while progressing toward a goal.

## Related Concepts

- [[Waypoint Prediction]] ⚠️
- [[Local Navigation]] ⚠️
- [[Occupancy Grid Map]] ⚠️ ⚠️ — a more detailed alternative representation; often used as source for the abstract map
- [[Cost Map]] ⚠️ — another abstraction used in path planning

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Abstract Obstacle Map` --[[related_to]] ⚠️--> `Abstract Obstacle Map-Based Waypoint Predictor` _(wikilink)_