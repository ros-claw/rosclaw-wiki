---
id: nesy_task_planner
title: NeSy task planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:22:55'
last_reinforced: '2026-04-30T00:22:55'
supersedes: []
sources:
- papers/2502.00931.pdf
source_type: arxiv_paper
---

## NeSy Task Planner

The **NeSy task planner** is a neuro-symbolic algorithm designed for robotic task planning and execution. It leverages a [[symbolic 3D scene graph]] and an [[image memory system]] to enhance the neural reasoning capabilities of a [[VLM]] ⚠️ ⚠️ for **task decomposition** and **replanning** in dynamic environments.

### Capabilities

- **Task decomposition**: Breaks high-level goals into executable sub-tasks using symbolic scene understanding.
- **Replanning**: Dynamically adjusts plans when execution fails or environment changes occur, using stored image memories to inform new decisions.

### Relationships

- **Uses**: [[symbolic 3D scene graph]], [[image memory system]], [[VLM]] ⚠️ ⚠️
- **Part of**: [[VL-Nav]]

### Description

The NeSy task planner integrates symbolic scene graphs (providing structured spatial knowledge) with an image memory system that retains visual snapshots from prior interactions. This combined representation is fed into a vision-language model (VLM), which performs neural reasoning to generate and revise task plans. The planner outputs a sequence of actions that respect both geometric constraints and semantic task requirements.

By grounding symbolic knowledge in visual memories, the planner improves generalization and robustness compared to purely symbolic or purely neural approaches. It is specifically designed as the reasoning backbone of the [[VL-Nav]] navigation system, enabling complex long-horizon tasks with real-time adaptability.