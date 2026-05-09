---
id: vln_ce
title: VLN-CE
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:21'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.19655.pdf
source_type: arxiv_paper
---

## VLN-CE

**VLN-CE** (Vision-and-Language Navigation in Continuous Environments) is a benchmark and task framework that requires an agent to navigate through previously unseen 3D environments using only natural language instructions, without any prior training in those spaces. It extends the classic [[Vision-and-Language Navigation]] (VLN) problem from discrete graph-based worlds to continuous, physics-realistic environments, adding significant challenges in perception, planning, and grounding.

### Definition

Vision-and-Language Navigation in Continuous Environments (VLN-CE) is a benchmark task where an agent must navigate through unseen continuous environments following natural language instructions without any prior training.

### Description

VLN-CE is a benchmark for zero-shot vision-and-language navigation in continuous environments. Agents must interpret free-form linguistic commands and execute a sequence of actions (e.g., move forward, turn) in an open world, adapting to novel layouts and obstacles. The benchmark is designed to test generalization: no environment in the test set is seen during training. It is closely related to the [[House3D]] ⚠️ and [[Matterport3D]] ⚠️ simulators and is often used in [[Sim-to-Real]] ⚠️ transfer research.

### Capabilities

- Requires agent to navigate unseen environments based on natural language instructions without prior training.
- Evaluates navigation agents in unseen continuous environments, demanding real-time perception (RGB-D or panorama), spatial reasoning, and grounding of language to continuous coordinates.
- Supports evaluation of both model-based and end-to-end learning approaches.

### Relationships

- **uses** [[Continuous Control]] ⚠️ for action execution.
- **depends_on** [[Scene Understanding]] ⚠️ and [[Language Grounding]] ⚠️.
- **implements** the [[Zero-Shot Generalization]] ⚠️ paradigm in embodied AI.
- **part_of** the broader field of [[Embodied AI]].
- **requires** [[Visual Perception]] ⚠️ to parse the continuous environment, along with natural language instructions for goal specification.
- **used_by** the [[LaViRA]] system, which benchmarks its navigation capabilities on this task.

### Key Challenges

- Bridging the gap between discrete language instructions and continuous state spaces.
- Handling dynamic obstacles and partial observability.
- Achieving robust navigation without environment-specific supervision.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLN-CE` --[[related_to]] ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `VLN-CE` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`