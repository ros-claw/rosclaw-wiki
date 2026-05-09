---
id: neurosymbolic_planning
title: Neurosymbolic Planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:31:43'
last_reinforced: '2026-04-30T00:31:43'
supersedes: []
sources:
- papers/2509.18592.pdf
source_type: arxiv_paper
---

# Neurosymbolic Planning

**Neurosymbolic Planning** is a hybrid approach that combines neural network-based perception and reasoning with symbolic planning techniques. In embodied intelligence, it enables agents to generate executable navigation plans by reasoning over structured representations such as scene graphs, without requiring task-specific training data.

## Overview

Unlike purely end-to-end neural methods, neurosymbolic planning leverages explicit symbolic representations (e.g., scene graphs) to ground high-level goals into actionable sequences. The neural component handles perception and ambiguity, while the symbolic component enforces logical constraints and produces interpretable plans. This paradigm is particularly suited for zero-shot generalization in vision-language navigation tasks.

## Key Parameters

- **Mode**: zero-shot neurosymbolic navigation  
  The planner operates without prior exposure to the target environment, using only a scene graph and current observations.

## Capabilities

- Reason over [[Scene Graphs]] and environmental observations to infer spatial relationships, object locations, and action affordances.
- Generate executable plans (e.g., sequences of movement commands) that satisfy a given natural language instruction.

## Relationships

- **Used by** → [[VLN-Zero]]: The [[VLN-Zero]] system implements a neurosymbolic planner to achieve zero-shot vision-language navigation.
- **Depends on** → [[Scene Graphs]]: The planner requires a structured scene graph as input, which encodes objects, their attributes, and spatial relations.

## Deployment Phase

In deployment, a neurosymbolic planner reasons over the scene graph and observations to produce plans. The process typically involves:

1. Parsing a natural language instruction into a high-level goal.
2. Querying the [[Scene Graphs|scene graph]] to identify relevant objects and paths.
3. Applying symbolic reasoning (e.g., predicate logic, action sequencing) to generate a step-by-step plan.
4. Executing the plan via low-level control while monitoring observations for failure or replanning.

This design eliminates the need for environment-specific fine-tuning, making it robust across diverse scenes.

## See Also

- [[VLN-Zero]]
- [[Scene Graphs]]
- [[Embodied AI]]
- [[Zero-Shot Navigation]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Neurosymbolic Planning` --[[related_to]] ⚠️--> `Embodied AI`
