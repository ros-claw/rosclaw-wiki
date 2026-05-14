---
id: mllms
title: MLLMs
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:07:59'
last_reinforced: '2026-04-30T00:07:59'
supersedes: []
sources:
- papers/2510.19655.pdf
source_type: arxiv_paper
---

## MLLMs (Multimodal Large Language Models)

**MLLMs** (Multimodal Large Language Models) are a class of foundation models that extend the reasoning and generation capabilities of large language models to multiple modalities—most commonly vision and language, but also including audio, tactile, and proprioceptive signals. In the context of Embodied AI, MLLMs serve as a bridge between high-level symbolic reasoning and low-level sensorimotor control.

### Capabilities

Recent MLLMs exhibit three core capabilities that are particularly relevant for robotic systems:

- **Reasoning** – Chain-of-thought, spatial, and causal reasoning over multimodal inputs.
- **Perceptual grounding** – Connecting linguistic concepts to visual and physical entities (e.g., "the red cup on the left").
- **Low-level control** – Outputting motion primitives, joint angles, or end-effector trajectories directly from language instructions.

### Parameters

Different scales of MLLMs (in terms of parameter count and training data) are used depending on the task. Larger models excel at complex reasoning but are slower; smaller models are more suitable for real-time control.

### Role in LaViRA

In the LaViRA framework, MLLMs are employed at multiple stages, each leveraging a different scale to maximize performance for the specific subtask:

- **Reasoning stage**: A large-scale MLLM handles high-level task decomposition and semantic understanding.
- **Perceptual grounding stage**: A mid-scale MLLM relates language to visual features and object affordances.
- **Low-level control stage**: A compact MLLM produces fast, reactive motor commands.

This cascaded use enables LaViRA to combine the strengths of different MLLM scales while maintaining computational efficiency.

### Related Entities

- LaViRA – uses MLLMs as described above.
- Embodied AI – the broader field where MLLMs are applied.
- VLA Model ⚠️ – a related concept integrating vision, language, and action.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MLLMs` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `MLLMs` --related_to ⚠️ ⚠️--> `LaViRA` _(wikilink)_
