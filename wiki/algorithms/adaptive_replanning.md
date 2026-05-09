---
id: adaptive_replanning
title: Adaptive Replanning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:52:24'
last_reinforced: '2026-04-30T03:52:24'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

# Adaptive Replanning

**Adaptive Replanning** is an algorithm for dynamic plan adjustment in robotic navigation. It is a core component of [[AINav]], providing flexibility and autonomy in response to changing environments or task requirements.

## Parameters

The algorithm consists of two LLM-based modules:

- **[[Advisor]]**: Determines *when* replanning is needed, acting as a flexible trigger.
- **[[Arborist]]**: Performs the actual plan adjustment by adding or removing nodes in the primitive [[skill tree]] ⚠️ ⚠️.

## Capabilities

- Flexible replanning trigger (via [[Advisor]])
- Autonomous plan adjustment (via [[Arborist]])
- Rapid plan adaptation through node addition and pruning in the [[skill tree]] ⚠️ ⚠️

The system supports efficient, online adaptation without requiring full recomputation from scratch.

## Relationships

- `part_of`: [[AINav]]
- `uses`: [[Large Language Models]] (to drive both modules)

## Mechanism

Adaptive Replanning employs two LLM-based modules in sequence:

1. **Advisor** monitors the current navigation state (e.g., obstacles, goal changes, time constraints) and decides whether a replan is justified. If triggered, it passes context to the Arborist.
2. **Arborist** modifies the existing plan by inserting new primitive skill nodes or removing outdated ones in the skill tree. This tree structure enables targeted, surgical changes, minimizing disruption while maintaining plan feasibility.

The combination allows for both judicious triggering and efficient execution, making the approach suitable for real-time robotic systems.