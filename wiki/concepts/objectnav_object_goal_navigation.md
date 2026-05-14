---
id: objectnav_object_goal_navigation
title: ObjectNav (Object Goal Navigation)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:37:59'
last_reinforced: '2026-04-29T20:37:59'
supersedes: []
sources:
- papers/2509.16445.json
source_type: arxiv_paper
---

# ObjectNav (Object Goal Navigation)

**Object Goal Navigation** (ObjectNav) is a fundamental task in Embodied AI in which an agent must navigate to a specific object instance or category within an unfamiliar environment. The agent receives a goal specification (e.g., "‘find the cup’") and relies on its perception, memory, and control policies to explore and locate the target. ObjectNav serves as a benchmark for evaluating spatial reasoning, exploration strategies, and generalisation to unseen layouts.

## Capabilities
- Navigate to a specified object (class or instance) in a previously unknown environment.
- Integrate visual observations, semantic understanding, and path planning to efficiently reach the goal location.

## Role in FiLM-Nav
ObjectNav is a component of the **FiLM-Nav training data mixture**. Within this mixture, ObjectNav episodes provide supervised signals for learning robust navigation policies that condition on object categories, helping the model generalise across diverse scenes and object types.

## Related Concepts
- ObjectGoalNav ⚠️ — synonymous term.
- PointGoal Navigation ⚠️ — a similar task where the goal is a 2D coordinate rather than an object.
- ImageGoal Navigation ⚠️ — the goal is a target image of the object.
- Embodied AI — the broader field encompassing ObjectNav.
- Sim-to-Real ⚠️ — often used when deploying ObjectNav policies from simulation to physical robots.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `ObjectNav (Object Goal Navigation)` --related_to ⚠️--> `FiLM-Nav` _(wikilink)_
