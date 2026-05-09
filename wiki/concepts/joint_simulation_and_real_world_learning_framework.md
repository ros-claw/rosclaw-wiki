---
id: joint_simulation_and_real_world_learning_framework
title: Joint Simulation and Real-World Learning Framework
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:18:49'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1910.09664.pdf
source_type: arxiv_paper
---

# Joint Simulation and Real-World Learning Framework

The **Joint Simulation and Real-World Learning Framework** is a learning approach for embodied instruction following that integrates data from both [[Simulation]] ⚠️ ⚠️ and [[Real Environment|real environments]] to train models capable of performing physical tasks. It is designed to bridge the gap between simulated training and real-world deployment, reducing or eliminating the need for autonomous operation in the real world during the training phase. The framework combines [[Supervised Learning]] ⚠️ ⚠️ techniques with [[Reinforcement Learning]] elements to achieve effective behavior.

## Overview

This framework leverages the strengths of both simulated and real-world data. Simulation provides unlimited, safe, and controllable training data, while real-world data grounds the model in actual physical dynamics. The framework learns a shared representation or policy that generalizes from simulation to reality without requiring the robot to fly or act autonomously in the real environment during training.

In its specific implementation for natural language–guided quadcopter control, the framework uses the [[SuReAL]] (Simulation and Real-World Alignment Learning) algorithm to map language instructions to low-level control commands. The framework takes raw first-person observations and navigation instructions as input and produces continuous control outputs.

## Capabilities

- **Sim-to-Real Transfer without Autonomous Real-World Training**: Enables training in simulation and deployment in the real world without requiring autonomous flight in the real environment during training. This avoids the risks and costs associated with early-stage real-world operation.
- **Data Integration**: Combines simulated experience with real-world demonstrations or corrections, improving robustness to domain shift.
- **Instruction-to-Control Mapping**: Maps natural language navigation instructions and raw first-person observations directly to continuous control commands.
- **Exploration Estimation**: Estimates the need for environment exploration based on instruction ambiguity or uncertainty.
- **Position Likelihood Prediction**: Predicts the likelihood of visiting specific positions in the environment during task execution.
- **Active Exploration**: Explores and visits high-likelihood positions to gather information and successfully complete tasks.

## Evaluation

The framework was evaluated on a natural language instruction-following task using a physical quadcopter. It demonstrated effective execution of complex navigation commands and exhibited sensible exploration behavior when instructions were ambiguous, confirming its ability to generalize from simulation to the real world.

## Relationships

- **Uses**: [[SuReAL]] — the specific algorithm employed to align simulated and real-world data representations.
- **Involves**: [[Simulation]] ⚠️ ⚠️ for synthetic data generation and safe exploration; [[Real Environment]] ⚠️ ⚠️ for grounding and validation; [[Supervised Learning]] ⚠️ ⚠️ for training on paired data; [[Reinforcement Learning]] for improving exploration and control.
- **Applied to**: Physical quadcopter navigation in the source paper.

## Applications

- **Language-Guided Quadcopter Control**: In the source paper ([[papers/1910.09664.pdf]] ⚠️), the framework is applied to map natural language instructions (e.g., "fly to the red marker") into control actions for a quadcopter. The model is trained in a simulator and deployed on a real drone without any autonomous flight data from the real world.

## References

- Original paper: *Language-guided Task Adaptation for Quadcopter Control via Simulation and Real-World Learning* (arXiv:1910.09664)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Joint Simulation and Real-World Learning Framework` --[[related_to]] ⚠️--> `SuReAL` _(wikilink)_