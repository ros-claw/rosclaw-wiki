---
id: dynamic_obstacle_avoidance
title: dynamic obstacle avoidance
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:26:42'
last_reinforced: '2026-04-30T00:26:42'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

## Dynamic Obstacle Avoidance

**Dynamic obstacle avoidance** refers to the capability of a robotic system to perceive and react to moving obstacles in real time, adjusting its planned trajectory to avoid collisions without replanning from scratch. This ability is critical for autonomous navigation in unstructured or human-populated environments.

### Key Characteristics

- **Real-time local decision-making** — Dynamic obstacle avoidance requires instantaneous responses to unexpected changes in the environment. This is enabled by a dual-system architecture ⚠️ where fast, reactive processes handle immediate threats.
- The system must balance between maintaining progress toward a global goal and safely deviating from the nominal path around moving objects.

### Capabilities

- adaptive navigation ⚠️ in dynamic environments — the robot can modify its motion based on sensor observations of obstacle velocity and direction.

### Relationships

- **enabled_by** System 1 — the reactive, high-speed component of a dual-system design that generates avoidance maneuvers without deliberation.
- **depends_on** real-time perception ⚠️ — requires accurate sensor data (e.g., LiDAR, depth cameras) and fast obstacle tracking.
- **implements** collision avoidance policy ⚠️ — many implementations use potential fields, velocity obstacles, or learning‑based reactive controllers.

### Source

- Paper `papers/2512.08186.pdf` — describes a dual-system framework where System 1 directly enables real-time local decision-making for dynamic obstacle avoidance.