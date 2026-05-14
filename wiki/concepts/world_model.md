---
id: world_model
title: world_model
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:06:49'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2403.07376.pdf
- papers/2512.01550.pdf
source_type: arxiv_paper
---

# world_model

The **world_model** concept refers to a predictive internal representation of the environment that an agent uses to simulate future states, imagine future scenarios, and reason about action consequences. World models are central to model-based reinforcement learning and planning, enabling agents to perform closed-loop decision-making without continuous direct sensory input.

## Definition
A world model is an internal representation of the environment that enables an agent to imagine future scenarios, often used in model-based reinforcement learning and planning. It captures the dynamics of the environment (transition model) and can be queried to predict what will happen next given the current state and a candidate action.

## Capabilities
- Predicts future observations and states.
- Simulates the consequences of possible actions.
- Provides internal foresight for planning and decision-making.
- In the context of NavCoT, the world model is implemented via an Large Language Model (LLM), which acts as a generative model to imagine plausible next observations based on the current observation and the given high-level instruction.
- Enables the agent to reason about future states without direct sensory input, facilitating closed-loop decision making.

## Parameters
- **Usage**: The world model is employed as the "imagination" component in NavCoT; it produces a candidate next observation that the agent uses to select the next action.
- The underlying representation may be learned (e.g., via neural networks) or symbolically grounded, depending on the framework.

## Role in Navigation Frameworks

### In NavCoT
In the NavCoT system, the LLM functions as a world model. Given an instruction (e.g., "go to the kitchen") and the current observation (e.g., "I see a hallway and a door on the left"), the world model predicts what the next observation should look like if the agent follows the instruction. This imagined observation is then used by the navigation policy to evaluate and choose the best action, enabling **self-guided** decision-making without an external simulator or explicit map.

### In NavForesee
The NavForesee framework also makes use of a world model to predict future observations and states, simulating the consequences of actions to provide internal foresight for planning. The world model in this context similarly enables the agent to reason about future scenarios without relying on an external simulation environment.

## Relationships
- **`used_by`**: NavCoT — the world model is a core component of the NavCoT pipeline.
- **`used_by`**: NavForesee — the world model is employed to provide foresight and simulate action consequences in navigation.
- **`depends_on`**: LLM ⚠️ ⚠️ — in some implementations, the world model is realized by a large language model that can generate coherent next‑step descriptions.
- **`related_to`**: Model-Based Reinforcement Learning ⚠️ — world models are a foundational component of model‑based approaches.

---

*Sources: arXiv paper 2403.07376, arXiv paper 2512.01550*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `world_model` --related_to ⚠️--> `NavCoT` _(wikilink)_
- `world_model` --used_by ⚠️--> `NavForesee` _(wikilink)_