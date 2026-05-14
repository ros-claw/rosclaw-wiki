---
id: multi_modal_large_models_mlms
title: Multi-modal Large Models (MLMs)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:08:41'
last_reinforced: '2026-04-30T03:08:41'
supersedes: []
sources:
- papers/2407.06886.pdf
source_type: arxiv_paper
---

# Multi-modal Large Models (MLMs)

**Multi-modal Large Models (MLMs)** are a class of foundation models trained on diverse data types — including text, images, video, audio, and sensor streams — enabling them to process and integrate information across multiple modalities. In the context of embodied intelligence, MLMs serve as a promising architecture for Embodied AI agents due to their remarkable capabilities in perception, interaction, and reasoning.

## Capabilities

MLMs exhibit three core capabilities:

- **Perception** — The ability to interpret and fuse inputs from multiple sensor modalities (e.g., camera images, LiDAR scans, tactile signals) into a unified representation.
- **Interaction** — The capacity to produce outputs that guide or control physical actions, such as generating motor commands or natural language instructions for Robotic Manipulation ⚠️ tasks.
- **Reasoning** — The capacity to perform high-level reasoning over multimodal inputs, including spatial reasoning, causal inference, and planning, often leveraging Large Language Models as a backbone.

## Role

Multi-modal Large Models are a promising architecture for embodied agents because they unify perception, language understanding, and action generation within a single learned representation. By bridging the gap between raw sensory data and symbolic reasoning, MLMs enable more flexible and generalizable behavior in unstructured environments. They are increasingly used in systems such as RT-2 ⚠️ and PaLM-E ⚠️ to drive real-world robot control.

## Dependencies

MLMs depend on large-scale pretraining on diverse multimodal datasets, powerful hardware for inference (e.g., GPU Clusters ⚠️), and alignment techniques to ground outputs in physical reality. They also rely on advances in Vision-Language Models ⚠️ ⚠️ and Transformer Architectures ⚠️.

## Related Algorithms

- Vision-Language Models ⚠️ ⚠️ — Often serve as the visual backbone for MLMs.
- Embodied Foundation Models ⚠️ — Extend MLMs with action spaces for robotics.
- Robot Learning ⚠️ — MLMs are applied to imitation learning, reinforcement learning, and task planning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multi-modal Large Models (MLMs)` --based_on ⚠️--> `Embodied AI`
