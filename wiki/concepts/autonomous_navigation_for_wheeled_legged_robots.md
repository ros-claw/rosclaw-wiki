---
id: autonomous_navigation_for_wheeled_legged_robots
title: Autonomous Navigation for Wheeled-Legged Robots
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:43:10'
last_reinforced: '2026-04-29T21:43:10'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

# Autonomous Navigation for Wheeled-Legged Robots

**Autonomous Navigation for Wheeled-Legged Robots** refers to the integrated control and planning framework that enables wheeled-legged platforms (e.g., robots with both wheeled and legged locomotion) to navigate autonomously over long distances in complex, unstructured urban environments. This concept combines locomotion control, motion planning, and high-level navigation to achieve continuous, robust traversal of kilometer-scale routes while adapting to varied terrain and dynamic obstacles.

## Key Capabilities

- **Integrated locomotion and navigation control** – the system couples low-level leg/wheel coordination with high-level path planning, allowing seamless transitions between walking, rolling, and hybrid modes.
- **Real-world validation over long distances** – demonstrated in field tests covering multiple kilometers in urban settings, showing reliability beyond laboratory conditions.
- **Adaptability to varied urban terrains and dynamic obstacles** – handles curbs, stairs, uneven pavement, pedestrian traffic, and other common city challenges without manual intervention.

## Dependencies and Related Concepts

This concept builds on several foundational technologies: it depends on:

- **[[Hierarchical Reinforcement Learning]]** – used to train locomotion policies that can switch between gait modes and adapt to terrain.
- **[[Adaptive Locomotion Control]]** – provides real‑time adjustment of leg stiffness, foot placement, and wheel speeds based on ground feedback.
- **[[Mobility-Aware Local Navigation Planning]]** – a planner that considers the robot’s current mobility capabilities (e.g., ability to climb a curb or roll over a smooth surface) when choosing short‑term trajectories.
- **[[Large-Scale Path Planning]]** – a global planner that generates kilometer‑scale routes through city street networks, accounting for robot size, power constraints, and terrain constraints.

## Significance

The successful deployment of wheeled-legged robots for autonomous navigation at urban scale demonstrates the feasibility of applying such platforms to **last-mile delivery** and **autonomous logistics** in city environments. By combining the speed of wheels with the agility of legs, these robots can overcome obstacles that stymie purely wheeled or legged systems, opening the door to cost‑effective, contact‑based urban logistics.

## Known Applications

- **Zurich and Seville field tests** – the concept was validated in real‑world trials covering several kilometers in these cities, showcasing adaptability to European urban layouts.
- **Last‑mile delivery** – the ability to navigate sidewalks, cross streets, and handle curbs makes wheeled‑legged robots ideal candidates for package delivery in pedestrian‑dense areas.

---

*Source: arXiv paper 2405.01792 – "Autonomous Navigation for Wheeled-Legged Robots at Kilometer Scale"*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Autonomous Navigation for Wheeled-Legged Robots` --[[related_to]] ⚠️--> `Hierarchical Reinforcement Learning` _(wikilink)_
