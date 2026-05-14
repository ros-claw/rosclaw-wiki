---
id: high_level_task_planning
title: High-level task planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:33:26'
last_reinforced: '2026-04-30T04:33:26'
supersedes: []
sources:
- papers/2405.14093.pdf
source_type: arxiv_paper
---

## High-level Task Planning

**High-level task planning** refers to the process of breaking down a long-horizon, complex goal into an ordered sequence of subtasks or primitive actions, often without specifying low-level motor commands. It serves as the reasoning layer that decides *what to do*, while lower-level controllers handle *how to do it*. In the context of Embodied AI and Vision-Language-Action Models ⚠️, high-level planners translate natural-language or symbolic goals into actionable plans that can be executed by robots.

### Capabilities

- **Decomposing long-horizon tasks into subtasks** – The planner recursively decomposes a high‑level objective (e.g., “make coffee”) into a temporally ordered set of subgoals (e.g., “grab cup”, “fill coffee maker”, “turn on machine”). This decomposition is essential for handling tasks that span many seconds to minutes.

### Relationships

- **Part of** – High‑level task planning is a key component of Vision-Language-Action Model based task planners ⚠️, which integrate visual perception, language grounding, and action execution into a single end‑to‑end framework. In such systems, the planner acts as the cognitive orchestrator that calls upon Low‑level motion controllers ⚠️ or Manipulation skills ⚠️ to achieve each subtask.

### Context in the ROSClaw Knowledge Base

High‑level task planning is closely related to:

- Task and Motion Planning ⚠️ (TAMP), where discrete task plans are coupled with continuous motion trajectories.  
- Hierarchical Reinforcement Learning, which also learns to decompose tasks into sub‑policies.  
- LLM‑based planners ⚠️ (e.g., using Large Language Models to generate plans from language instructions).  

The inclusion of this concept in the ROSClaw Wiki supports reasoning about how Unitree G1 or a UR5 ⚠️ arm could sequence actions when given a high‑level command like “pick and place the red block.”

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `High-level task planning` --related_to ⚠️ ⚠️--> `Embodied AI`
- `High-level task planning` --applies_to ⚠️--> `Unitree G1`
**Pending review:**
- `High-level task planning` --related_to ⚠️ ⚠️--> `Hierarchical Reinforcement Learning` _(wikilink)_
