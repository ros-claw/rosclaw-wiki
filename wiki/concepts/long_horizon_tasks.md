---
id: long_horizon_tasks
title: Long-Horizon Tasks
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:04:05'
last_reinforced: '2026-04-30T04:04:05'
supersedes: []
sources:
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# Long-Horizon Tasks

**Long-Horizon Tasks** are complex missions that span multiple actions and require sustained attention to goals over extended time periods. They represent one of the core challenges in embodied AI and robotics, where an agent must perform sequential decision-making across many steps to achieve a final objective.

## Definition

Complex missions that span multiple actions and require sustained attention to goals. In contrast to short-horizon or single-step tasks, long-horizon tasks involve decomposing a high-level goal into a sequence of sub-goals, executing them in order, and adapting to changing conditions without losing sight of the ultimate objective.

## Capabilities

- Tasks requiring sequential decision-making over extended time and multiple sub-goals

## Relationships

Long-Horizon Tasks are addressed by the following approaches:

- **Hierarchical Task Planning** — Divides long-horizon missions into manageable sub-tasks, each executed by lower-level policies or controllers. This abstraction reduces the complexity of planning over long horizons.
- **LOVON** — A framework specifically designed to handle long-horizon tasks through learned hierarchical representations and goal-conditioned policies, enabling robots to maintain coherence across extended action sequences.

## Context

Long-horizon tasks are central to real-world applications such as household cleaning, assembly lines, and autonomous exploration. Success requires not only robust planning but also perception, memory, and error recovery mechanisms to handle the uncertainty that accumulates over many steps.