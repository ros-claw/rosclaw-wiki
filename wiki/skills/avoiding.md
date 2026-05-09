---
id: avoiding
title: Avoiding
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T00:20:47'
last_reinforced: '2026-04-30T00:20:47'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

# Avoiding

**Avoiding** is a navigational skill that enables an agent to detect and steer clear of obstacles within its environment. It is a core component of the [[MM-Nav]] capabilities suite, responsible for ensuring collision-free movement during task execution.

The skill is learned from an [[RL expert]] ⚠️ ⚠️ specifically trained in obstacle avoidance contexts. The expert policy, typically derived from reinforcement learning in simulation, provides the behavioral foundation for the agent’s avoidance decisions.

## Capabilities

- **Obstacle detection and avoidance**: The agent can perceive static and dynamic obstacles and adjust its path accordingly.

## Relationships

- **Part of**: [[MM-Nav]] capabilities – Avoiding is one of the fundamental navigation skills that compose the overall multi-modal navigation system.
- **Learned from**: [[RL expert]] ⚠️ ⚠️ trained in avoiding environment – The avoidance policy is distilled or fine-tuned from a reinforcement learning expert that was trained in environments requiring active obstacle avoidance.

## Usage Notes

Avoiding is invoked whenever the navigational planner predicts a potential collision. It may be co-activated with other skills such as [[Following]] ⚠️ or [[Exploring]] ⚠️ depending on the mission context. The skill relies on sensor inputs (e.g., depth cameras, LiDAR) and outputs velocity commands that steer the robot away from obstacles.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Avoiding` --[[uses]] ⚠️--> `MM-Nav`
