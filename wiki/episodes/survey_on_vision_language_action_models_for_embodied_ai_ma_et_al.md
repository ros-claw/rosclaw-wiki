---
id: survey_on_vision_language_action_models_for_embodied_ai_ma_et_al
title: Survey on Vision-Language-Action Models for Embodied AI (Ma et al.)
type: episode
tags: []
confidence: 0.8
created_at: '2026-04-30T04:34:01'
last_reinforced: '2026-04-30T04:34:01'
supersedes: []
sources:
- papers/2405.14093.pdf
source_type: arxiv_paper
---

## Survey on Vision-Language-Action Models for Embodied AI (Ma et al.)

This comprehensive survey by Ma et al. provides a systematic taxonomy of **Vision-Language-Action (VLA) models**, which form a critical component of modern [[Embodied AI]] systems. VLAs integrate visual perception, natural language understanding, and motor control into a unified framework, enabling robots and agents to perform complex tasks in real-world environments based on high-level instructions and visual inputs.

### Summary

The survey offers a taxonomy of VLAs that covers:
- Individual components
- Control policies
- Task planners

It also catalogues relevant datasets, simulators, and benchmarks, and discusses key challenges and future research directions. A curated repository is maintained at [https://github.com/yueen-ma/Awesome-VLA](https://github.com/yueen-ma/Awesome-VLA).

### Taxonomy Overview

The paper decomposes VLA systems into three primary layers:

1. **Perception & Representation** – how visual and linguistic inputs are encoded (e.g., using pretrained [[Vision-Language Models]] ⚠️ ⚠️ like CLIP or multimodal transformers).
2. **Reasoning & Planning** – task planning and sequencing using [[Large Language Models]] or learned policies.
3. **Action Execution** – low-level control policies that output motor commands or skill parameters.

The taxonomy further distinguishes between **end-to-end** VLA architectures and **modular** designs where components are trained separately and composed at inference time.

### Key Components

- **Vision Encoders**: Typically convolutional or transformer-based backbones (e.g., ViT, ResNet).
- **Language Encoders**: Often derived from large language models (e.g., GPT, T5).
- **Fusion Modules**: Cross‑attention or multimodal transformers align visual and linguistic features.
- **Policy Heads**: Map fused features to action spaces (continuous joint torques, discrete high-level actions, etc.).

### Datasets, Simulators & Benchmarks

The survey compiles a comprehensive list of resources, including:

- **Datasets** for VLA training (e.g., RLBench, CALVIN, MetaWorld, task-specific kitchen datasets).
- **Simulators** such as [[MuJoCo]] ⚠️, [[Isaac Gym]] ⚠️, [[Habitat]], and [[PyBullet]] ⚠️, which provide physics-realistic environments for training and evaluation.
- **Benchmarks** like [[MetaWorld]] ⚠️, [[BabyAI]] ⚠️, and [[ALFRED]] ⚠️ for task completion and generalization.

### Challenges & Future Directions

The authors highlight unresolved issues:

- **Generalization** across diverse objects, layouts, and instructions.
- **Data efficiency** – current models require large amounts of expensive robot interaction data.
- **Safety and robustness** in open-ended environments.
- **Integration with longer-horizon task planning** and commonsense reasoning.
- **Real‑time inference** constraints for deployment on physical robots.

### Related Pages

- [[Embodied AI]] – broader field encompassing VLAs.
- [[Vision-Language Models]] ⚠️ ⚠️ – foundation for multimodal perception.
- [[Task Planning]] ⚠️ – high-level reasoning for VLA sequences.
- [[Sim-to-Real Transfer]] – challenge addressed by many VLA works.
- [[Action Models]] ⚠️ – general concept for policy learning.

### Reference

Ma, Y, et al. "A Survey on Vision-Language-Action Models for Embodied AI." arXiv:2405.14093, 2024.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Survey on Vision-Language-Action Models for Embodied AI (Ma et al.)` --[[related_to]] ⚠️--> `Embodied AI` _(wikilink)_
