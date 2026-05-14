---
id: mixture_of_experts
title: Mixture of Experts
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:48:57'
last_reinforced: '2026-04-30T00:48:57'
supersedes: []
sources:
- papers/2412.05552.pdf
source_type: arxiv_paper
---

# Mixture of Experts (MoE)

**Type:** concept  
**Tags:** #neural-network-architecture, #multi-expert, #gating-mechanism, #efficient-inference

**Related Pages:** State-Adaptive Mixture of Experts (SAME), Gating Network ⚠️ ⚠️, Expert Network ⚠️, Neural Network Architecture ⚠️

---

## Overview

Mixture of Experts (MoE) is a neural network architecture that improves parameter efficiency and task specialization by routing each input to a subset of expert sub-networks. A learned gating function determines which experts to activate, enabling the model to combine shared knowledge from a common backbone with specialized modules that handle diverse input patterns.

## Architecture

An MoE block typically consists of:

- **Multiple expert networks** — parallel feed-forward or transformer layers, each potentially specializing in a different sub-task.
- **A gating / routing mechanism** — a differentiable function that outputs a sparse weight vector over experts, selecting one or a few per input.

The routing can be learned end-to-end, often with constraints (e.g., load balancing loss) to ensure experts are utilized evenly.

## Capabilities

- **Parameter efficiency** — only a fraction of the total parameters are activated for any given input, allowing very large models without proportional compute cost.
- **Task modularity** — experts can develop specialized representations for distinct instruction types, environmental conditions, or behavioral modes.
- **Transfer learning** — the shared backbone (e.g., a common transformer) captures general knowledge, while experts adapt to specific domains.

## Variants

### State-Adaptive Mixture of Experts (SAME)

In the context of navigation, State-Adaptive Mixture of Experts (SAME) extends MoE by conditioning the routing on both the robot’s **observation** (e.g., sensor data) and the **language instruction**. This allows the model to dynamically select expert policies tailored to the current scene and goal, improving generalization across diverse environments and instruction complexities.

SAME uses a state-adaptive router that replaces the standard learned gating with a function that processes the combined state (vision + language) before selecting experts. This variant is specifically designed for embodied navigation tasks and demonstrates superior performance on benchmarks like Vision-and-Language Navigation (VLN).

## Relationships

- State-Adaptive Mixture of Experts (SAME) **implements** Mixture of Experts.
- MoE **depends on** a Gating Network ⚠️ ⚠️ for expert selection.
- MoE **improves** over monolithic models by enabling modular specialization.

## Benefits in Embodied AI

- **Robustness**: Experts can handle failure modes independently (e.g., one expert for instruction-following, another for obstacle avoidance).
- **Scalability**: Adding new skills corresponds to adding a new expert without retraining the entire network.
- **Interpretability**: The gating weights can reveal which behavioral mode the robot is relying on at a given moment.

For more detail on the SAME variant, see the dedicated State-Adaptive Mixture of Experts (SAME) page.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Mixture of Experts` --related_to ⚠️--> `State-Adaptive Mixture of Experts (SAME)` _(wikilink)_
