---
id: supervised_reinforcement_asynchronous_learning
title: Supervised Reinforcement Asynchronous Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:45:16'
last_reinforced: '2026-04-30T02:45:16'
supersedes: []
sources:
- papers/1910.09664.pdf
source_type: arxiv_paper
---

## Supervised Reinforcement Asynchronous Learning (SRAL)

**Supervised Reinforcement Asynchronous Learning** (SRAL) is a hybrid algorithm that combines [[Supervised Learning]] ⚠️ ⚠️ for position prediction with [[Reinforcement Learning]] for continuous control in the context of instruction-following autonomous flight. It enables a [[Quadcopter]] ⚠️ to map natural language instructions and first-person observations to continuous flight commands without requiring autonomous flight in the physical environment during training.

### Overview

SRAL addresses the challenge of grounding natural language instructions in continuous, real-world robot control. It decomposes the task into two complementary components: a supervised model that predicts which positions in the environment are likely to be relevant during execution, and a reinforcement learning policy that drives the agent to visit those positions. The system is trained jointly in simulation and real environments, leveraging simulated flight to avoid the costs and risks of autonomous physical flight during the learning phase.

### Parameters

- **Composition**: Supervised learning for position prediction + Reinforcement learning for continuous control.
- **Training Requirement**: No autonomous flight in the physical environment during training.
- **Framework**: Joint simulation and real-world learning ([[Sim-to-Real]] ⚠️ ⚠️).

### Capabilities

- Maps natural language instructions and first-person observations to continuous control commands.
- Estimates the need for environment exploration based on the instruction.
- Predicts likelihood of visiting positions during execution.
- Controls the agent to explore and visit high-likelihood positions.

### Training Process

Learning uses both simulation and real environments without requiring autonomous flight in the physical environment during training. The process combines **supervised learning** for predicting positions to visit (e.g., a supervised map or waypoint predictor) and **reinforcement learning** for continuous control (e.g., a policy that outputs motor commands). This asynchronous setup allows the system to leverage large amounts of simulated data while also fine-tuning on real-world observations.

### Relationships

- **Uses**: [[Simulated Flight]] ⚠️, [[Real Quadcopter]] ⚠️, [[First-Person Observations]] ⚠️
- **Implements**: [[Instruction Following]] ⚠️, [[Continuous Control Mapping]] ⚠️
- **Depends on**: [[Supervised Learning]] ⚠️ ⚠️, [[Reinforcement Learning]], [[Sim-to-Real]] ⚠️ ⚠️ transfer techniques
- **Related to**: [[Embodied AI]], [[Vision-Language Models]] ⚠️, [[Asynchronous Learning]] ⚠️

### References

- Original paper: *Supervised Reinforcement Asynchronous Learning* (arXiv:1910.09664)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Supervised Reinforcement Asynchronous Learning` --[[based_on]] ⚠️--> `Embodied AI`
