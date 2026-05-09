---
id: zero_shot_embodied_navigation
title: Zero-Shot Embodied Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:51:30'
last_reinforced: '2026-04-30T03:51:30'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

# Zero-Shot Embodied Navigation

**Zero-Shot Embodied Navigation** is a paradigm for enabling an embodied agent to navigate to unseen goals or targets without any task-specific reinforcement learning (RL) training. It supports **open-vocabulary generalization**, meaning the agent can follow instructions or navigate to objects described in natural language without having been explicitly trained on those specific phrases or object categories.

## Description

Zero-Shot Embodied Navigation eliminates the need for per-task RL training, which is typically expensive and time-consuming. Instead, it leverages large-scale pretrained models and compositional reasoning to interpret arbitrary language commands and translate them into actionable navigation policies. This approach drastically improves the generality and sample efficiency of embodied agents, making them practical for real-world deployment where tasks vary unpredictably.

The method [[MSGNav]] implements Zero-Shot Embodied Navigation by combining a modular architecture with vision-language models, enabling the agent to parse open-vocabulary queries and plan paths in a zero-shot manner. MSGNav acts as a concrete instantiation of this paradigm, demonstrating that effective navigation can be achieved without any task-specific fine-tuning.

## Core Principles

- **No RL Training**: The agent does not undergo any reinforcement learning for the specific navigation task; instead, it relies on pretrained models and logical reasoning.
- **Open Vocabulary**: The system can understand any object or location described in natural language, not just a predefined set of categories.
- **Zero-Shot Transfer**: The agent can directly apply its knowledge to new environments and instructions without additional training.

## Relationship to Other Concepts

- Zero-Shot Embodied Navigation is a subfield of [[Embodied AI]] that focuses on navigation capabilities.
- It contrasts with traditional [[Navigation]] ⚠️ approaches that require task-specific [[Reinforcement Learning]] or explicit mapping.
- The paradigm depends on [[Vision-Language Models]] ⚠️ for grounding language to visual observations.
- It relates to [[Sim-to-Real Transfer]] by enabling trained models to operate in novel real-world scenes.

## Implemented By

- [[MSGNav]] — a modular zero-shot navigation system that realizes this paradigm.

## Future Directions

Zero-Shot Embodied Navigation opens the door to scalable, generalist navigation agents. Future work may integrate [[Graph Neural Networks]] ⚠️ for spatial reasoning or combine with [[Object Manipulation]] ⚠️ skills to achieve full embodied intelligence.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-Shot Embodied Navigation` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Zero-Shot Embodied Navigation` --[[related_to]] ⚠️ ⚠️--> `MSGNav` _(wikilink)_
