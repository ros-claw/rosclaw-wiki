---
id: ainav
title: AINav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:50:29'
last_reinforced: '2026-04-30T03:50:29'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

## Overview

AINav is an adaptive interactive navigation algorithm that enables robots to successfully traverse and reach goals in complex environments where no direct viable path exists. By proactively interacting with obstacles (e.g., pushing, nudging, climbing over small objects) and adapting its plan on the fly, AINav achieves originally unreachable objectives through intelligent re‑planning and real‑time obstacle manipulation.

The system integrates three core modules:

- **Adaptive Replanning** with an Advisor and Arborist component, which continuously evaluates plan feasibility and triggers re‑planning when obstacles block the current path.
- A **Primitive Skill Tree** that represents high‑level task structures and decomposes navigation goals into manageable sub‑tasks.
- A **Skill Library**, pre‑trained via **Reinforcement Learning**, that provides a repertoire of low‑level interaction skills (e.g., push, slide, climb) that the robot can execute to alter the environment.

AINav uses a **Large Language Model (LLM)** to interpret natural‑language navigation commands and to reason about alternative strategies when standard path planning fails. The combination of LLM‑driven reasoning, a structured skill tree, and RL‑trained interaction skills allows the robot to **adaptively interact with obstacles** rather than simply avoiding them, thereby creating new traversable routes.

### Capabilities

- Adaptive interactive navigation in complex environments with no viable paths
- Proactive interaction with the environment to create feasible paths
- Achieves originally unreachable goals through plan adaptation

### Relationships

- **Uses**: Large Language Models, Primitive Skill Tree, Skill Library, Adaptive Replanning
- **Depends on**: Reinforcement Learning

### How It Works

1. **Initial Task Planning**: The robot receives a navigation goal (e.g., “go to the kitchen”). An LLM interprets the command and generates a high‑level plan using the Primitive Skill Tree to decompose the goal into a sequence of sub‑tasks.
2. **Skill Execution**: The robot executes the sub‑tasks by calling skills from the Skill Library, which are pre‑trained via Reinforcement Learning to manipulate the environment (e.g., pushing a chair aside).
3. **Adaptive Replanning**: If the current skill fails (e.g., an obstacle cannot be moved in the expected way), the Advisor module detects the failure and the Arborist module proposes alternative actions — such as trying a different approach angle, combining two skills, or requesting human assistance.
4. **Interaction & Path Creation**: The robot physically interacts with obstacles (pushing, squeezing, or climbing over small objects) until a traversable path emerges, enabling it to reach goals that were initially unreachable.

This approach is particularly valuable in cluttered human environments (homes, offices, warehouses) where static path planning is insufficient and robots must actively reshape the workspace to accomplish their tasks.

### References

- Source paper: *AINav: Adaptive Interactive Navigation with LLM‑Guided Skill Trees* (arXiv:2503.22942)