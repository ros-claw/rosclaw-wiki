---
id: long_horizon_planning
title: long-horizon planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:28:10'
last_reinforced: '2026-04-30T00:28:10'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# Long-Horizon Planning

**Long-Horizon Planning** refers to the ability to plan over extended time horizons by reasoning about mid-term waypoint goals, as opposed to executing short-horizon discrete actions. This form of planning requires abstract reasoning, hierarchical task decomposition, and often relies on a slower, more deliberative cognitive process.

## Definition

Long-horizon planning involves generating a sequence of intermediate objectives (waypoints) that bridge the current state to a desired future state over many time steps or environmental changes. It contrasts with reactive or short-horizon methods that only consider immediate next actions.

## Key Characteristics

- **Extended temporal scope**: Plans may span minutes, hours, or even longer.
- **Waypoint goals**: Intermediate milestones that simplify the problem into manageable subproblems.
- **Abstract reasoning**: Requires understanding of causal relationships, dynamics, and constraints.
- **Deliberative computation**: Typically slower than reactive control, but yields more robust long-term behavior.

## Relationships

- **Achieved by** [[System 2]]. Long-horizon planning is a hallmark of System 2 thinking — slow, analytical, and rule-based — as opposed to the fast, intuitive responses of System 1.

## Related Concepts

- [[Task and Motion Planning]] ⚠️ (TAMP) — often integrates long-horizon symbolic planning with geometric reasoning.
- [[Hierarchical Reinforcement Learning]] — learns policies at multiple time scales.
- [[Waypoint Tracking]] ⚠️ — execution layer that follows the planned milestones.
- [[Model Predictive Control]] ⚠️ (MPC) — performs online receding-horizon optimization, a short-horizon counterpart.

## Usage in Embodied AI

In robotics and embodied agents, long-horizon planning enables systems to:

- Navigate complex environments with multiple subgoals (e.g., fetch-and-place tasks).
- Compose skills into coherent sequences (e.g., opening a door then picking an object).
- Reason about future consequences of actions (e.g., tool use, object rearrangement).

## Dependencies

Long-horizon planning depends on [[World Models]] to simulate outcomes, [[State Estimation]] ⚠️ to maintain belief about the environment, and often [[Semantic Scene Graphs]] ⚠️ for spatial reasoning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `long-horizon planning` --[[related_to]] ⚠️--> `Hierarchical Reinforcement Learning` _(wikilink)_
