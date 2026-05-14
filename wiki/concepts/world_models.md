---
id: world_models
title: World Models
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:29:30'
last_reinforced: '2026-04-30T04:29:30'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

## Definition

**World Models** are internal representations that enable an agent to predict future sensory observations and reward signals. By learning a compressed model of the environment, an agent can simulate possible futures without interacting with the real world, making them a cornerstone of model-based reinforcement learning and embodied intelligence.

## Capabilities

- **Imagination of future states and outcomes** – World models allow agents to "dream" about what will happen next, providing a mental rehearsal space for evaluating actions.
- **Planning and decision-making through simulation** – Instead of costly real-world trial-and-error, the agent can test multiple candidate trajectories within the world model and select the most promising one.

## Role in Navigation

In visual navigation, world models bridge perception and action by simulating the consequences of candidate actions. For example, a robot can query its world model: "If I turn left, what will I see?" and use the predicted visual outcome to decide whether to proceed. This reduces the need for exhaustive exploration and enables long-horizon planning in cluttered environments.

## Relationships

- **Uses**: Visual Foresight ⚠️ – World models often rely on visual foresight techniques to generate plausible future frames.
- **Depends on**: Memory-Augmented Planning – To maintain coherence over long sequences, world models require memory mechanisms that store and retrieve relevant past experiences.

## Further Reading

- Integration with Embodied AI frameworks
- Connection to Sim-to-Real Transfer when policies are trained entirely inside learned world models

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `World Models` --related_to ⚠️--> `Embodied AI`
