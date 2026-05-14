---
id: autonomous_drone_navigation
title: Autonomous Drone Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:01:42'
last_reinforced: '2026-04-30T00:01:42'
supersedes: []
sources:
- papers/2512.15258.pdf
source_type: arxiv_paper
---

# Autonomous Drone Navigation

**Autonomous Drone Navigation** refers to the capability of an unmanned aerial vehicle (UAV) to perceive its environment, plan a path, and execute self-directed flight toward a goal while avoiding obstacles—all without human intervention. It is a central challenge in Embodied AI and Robotics ⚠️ ⚠️, requiring integration of perception, planning, control, and onboard computation.

## Capabilities

- **Self-directed flight through complex environments** – the drone independently navigates cluttered or dynamic spaces.
- **Obstacle avoidance** – detects and maneuvers around obstacles in real time.
- **Goal reaching** – arrives at specified target coordinates or objects.

## Approaches

This problem is *addressed_by*:
- VLA-AN – a vision-language-action architecture specifically designed for autonomous drone navigation.

## Challenges

- **Domain gap** – models trained in simulation often fail in real-world conditions due to differences in visual appearance, physics, or dynamics.
- **Temporal reasoning** – drones must understand motion and predict future states of objects and the environment.
- **Safety** – ensuring collision-free flight and handling of edge cases (e.g., sensor failure, gusts of wind).
- **Onboard compute constraints** – limited battery and computational power restrict the complexity of models that can run in real time on a drone.

## Relationships

- *related_to*: Embodied AI, Robotics ⚠️ ⚠️
- *depends_on*: Computer Vision ⚠️, Path Planning ⚠️, Control Theory ⚠️
- *implements*: Autonomous Navigation ⚠️ in aerial platforms

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Autonomous Drone Navigation` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Autonomous Drone Navigation` --related_to ⚠️ ⚠️--> `VLA-AN` _(wikilink)_
