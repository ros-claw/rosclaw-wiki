---
id: embodied_visual_grounding
title: Embodied Visual Grounding
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:19:33'
last_reinforced: '2026-04-30T02:19:33'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

Embodied Visual Grounding is the task of linking natural language references to objects or locations in a physical environment through the sensorimotor capabilities of an embodied agent. It extends classical [[Visual Grounding]] by requiring the agent to actively perceive, move, and interact with the world, rather than processing static images. This concept sits at the intersection of [[Embodied AI]] and [[Vision-Language Models]] ⚠️ ⚠️ ⚠️, and is a critical component for systems that must follow natural language instructions in real-world settings.

## Capabilities

- Understanding visual environment and language jointly to carry out navigation and object localization.

## Functional Dependencies

- **Depends on** [[Visual Grounding]] for the core alignment of language expressions with visual features.
- **Depends on** [[Embodied AI]] frameworks that provide simulation environments (e.g., [[Habitat]], [[AI2-THOR]]) and physical robot platforms.
- **Uses** [[Vision-Language Models]] ⚠️ ⚠️ ⚠️ to produce joint embeddings of images and text.
- **Implements** tasks such as [[Visual Navigation]] (e.g., "Go to the red chair") and [[Object Referring]] ⚠️ ⚠️ (e.g., "Pick up the mug next to the keyboard").

## Relationship Annotations

- `depends_on` [[Visual Grounding]]
- `depends_on` [[Embodied AI]]
- `uses` [[Vision-Language Models]] ⚠️ ⚠️ ⚠️
- `implements` [[Visual Navigation]]
- `implements` [[Object Referring]] ⚠️ ⚠️

## Key Research Directions

The paper *"Embodied Visual Grounding: A Survey"* (arXiv:2103.12944) reviews benchmarks, models, and open challenges in this area. Common approaches include modular pipelines that separate navigation from grounding, end-to-end reinforcement learning, and large-scale pretraining on synthetic data. Open problems include generalization to unseen environments, efficient exploration, and handling ambiguous or context-dependent language.

## Related Concepts

- [[Sim-to-Real Transfer]] – crucial for deploying models trained in simulation onto physical robots.
- [[Grounded Language Learning]] ⚠️ – broader field of linking language to sensory-motor experience.
- [[Instruction Following]] ⚠️ – the task of executing step-by-step language commands in an environment.
- [[Semantic Mapping]] ⚠️ – building maps that contain not only geometry but also object labels and language-referable attributes.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Embodied Visual Grounding` --[[related_to]] ⚠️--> `Embodied AI`
