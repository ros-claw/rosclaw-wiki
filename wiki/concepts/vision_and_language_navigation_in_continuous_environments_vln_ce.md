---
id: vision_and_language_navigation_in_continuous_environments_vln_ce
title: Vision-and-Language Navigation in Continuous Environments (VLN-CE)
type: concept
tags: []
confidence: 0.9
created_at: '2026-04-29T20:58:59'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2506.23468.pdf
- papers/2408.10388.pdf
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# Vision-and-Language Navigation in Continuous Environments (VLN-CE)

## Overview

**Vision-and-Language Navigation in Continuous Environments (VLN-CE)** is an [[embodied AI]] research problem setting in which an agent must follow natural language instructions to navigate in continuous, realistic 3D environments without relying on discretized actions. It extends discrete [[Visual Language Navigation (VLN)]] ⚠️ ⚠️ by requiring continuous movement, obstacle avoidance, and deeper environmental understanding, rather than selecting from a predefined set of discrete locations. The agent must understand complex instructions, perceive its surroundings dynamically, and execute long-range plans with smooth motion control.

## Key Capabilities

A successful VLN‑CE agent must demonstrate:

- **Understanding of instructions** – parsing and grounding natural language to real‑world spatial relations and landmarks.
- **Obstacle avoidance** – reacting to dynamic and static obstacles in real time.
- **Long-range planning** – maintaining a global navigation strategy while executing fine‑grained local actions.

## Common Approaches

To bridge the gap between raw continuous observation and high‑level instruction following, many VLN‑CE systems employ a decomposition strategy:

1. **Discretize the environment** — A [[waypoint predictor]] estimates reachable locations (waypoints) from the agent’s current observation, converting the continuous space into a sparse set of viable steps.
2. **Simplify navigation into a view selection task** — Instead of continuous low‑level control, the agent selects which waypoint to move toward, effectively reducing the planning problem to a classification over candidate views.

This pipeline couples a learned representation of the scene with the language instruction, but the reliance on discretization can lead to misalignment between the predicted waypoints and the true free space. Alternative approaches use **[[Topological Maps]] ⚠️ ⚠️** to represent the environment at a higher level, enabling more abstract reasoning without fine‑grained waypoint prediction.

## Exemplary Methods

- **ETPNav** (Explicit Topological Planner for Navigation) – an example system that leverages topological graphs to plan long‑range paths while maintaining the continuous nature of motion execution. It demonstrates how VLN‑CE can be tackled by integrating language grounding, topological mapping, and continuous control.

## Relevance

VLN‑CE is a more practical and challenging variant of vision‑language navigation. By operating in continuous environments without discretized actions, it closely mirrors real‑world robotic deployment: the agent must perform smooth motion control, avoid obstacles, and react to environmental changes. Success in VLN‑CE therefore has direct implications for deploying [[instruction following]] ⚠️ ⚠️ on physical platforms such as [[Unitree Go2]] or [[Jackal UGV]] ⚠️.

## Related Concepts

- **part_of** → [[embodied AI navigation]] ⚠️ – VLN‑CE is a sub‑problem within the broader field of embodied navigation.
- **related_to** → [[Visual Language Navigation (VLN)]] ⚠️ ⚠️ – both tasks use natural language and visual inputs, but VLN‑CE operates in continuous space rather than on a graph of pre‑defined nodes.
- **depends_on** → [[scene understanding]] ⚠️, [[language grounding]] ⚠️, [[continuous control]] ⚠️ – the agent must parse instructions, perceive its surroundings, and execute fine‑grained motions.
- **uses** → [[waypoint predictor]], [[Topological Maps]] ⚠️ ⚠️ – common techniques for structuring the continuous space.
- **implements** → [[instruction following]] ⚠️ ⚠️ in the context of physical, mobile robots.

## Challenges

Because the environment is continuous and dynamic, VLN‑CE demands robust perception under viewpoint variation, real‑time replanning, and the ability to interpret grounding phrases that refer to non‑discrete landmarks (e.g., “walk past the table toward the kitchen”). Success requires tightly coupling vision, language, and action in a single reactive loop. The common practice of discretizing the environment, while pragmatic, creates a gap between perception and action — the discretized waypoints may not capture all feasible motions, and small errors in the waypoint prediction can propagate into navigation failures. Methods that rely on topological representations aim to mitigate this issue by reasoning at a higher level of abstraction.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Vision-and-Language Navigation in Continuous Environments (VLN-CE)` --[[related_to]] ⚠️ ⚠️--> `embodied AI`
- `Vision-and-Language Navigation in Continuous Environments (VLN-CE)` --[[applies_to]] ⚠️--> `Unitree Go2`
**Pending review:**
- `Vision-and-Language Navigation in Continuous Environments (VLN-CE)` --[[related_to]] ⚠️ ⚠️--> `waypoint predictor` _(wikilink)_
