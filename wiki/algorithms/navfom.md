---
id: navfom
title: NavFoM
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:53:29'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.12129.pdf
source_type: arxiv_paper
---

# NavFoM

**NavFoM** (Navigation Foundation Model) is a unified, cross-embodiment and cross-task navigation algorithm that processes multimodal inputs to enable a single model to perform multiple navigation tasks across different robot platforms. It leverages [[Vision-Language Models]] ⚠️ ⚠️ and introduces [[Identifier Tokens]] plus a [[Dynamic Sampling Strategy]] to achieve state-of-the-art performance without task-specific fine-tuning.

## Architecture

NavFoM employs a unified architecture that accepts multimodal navigation inputs from varying camera configurations and navigation horizons. It incorporates **identifier tokens** that embed both the camera view information of different embodiments and the temporal context of each task, allowing the model to adapt its processing to the specific robot and navigation scenario. This design enables the model to interpret natural language instructions alongside visual observations.

## Training

The model is trained on **eight million navigation samples** spanning four distinct embodiment categories:
- [[Quadrupeds]] ⚠️
- [[Drones]] ⚠️
- [[Wheeled Robots]] ⚠️
- Vehicles

These samples cover a diverse set of tasks:
- Vision-and-language navigation ([[VLN]] ⚠️)
- Object searching
- Target tracking
- Autonomous driving

This large-scale, diverse training set enables NavFoM to generalize without per-task fine-tuning, achieving robust cross-task performance.

## Inference & Token Management

To meet real-world deployment constraints, NavFoM includes a token management mechanism that controls all observation tokens using a dynamically adjusted sampling strategy under a limited token length budget. This ensures efficient inference while preserving critical visual information. The dynamic sampling strategy adapts the number of tokens based on task complexity and available budget, allowing the model to maintain high performance across varying hardware platforms.

## Capabilities

- **Cross-embodiment and cross-task navigation** – works out-of-the-box on quadrupeds, drones, wheeled robots, and vehicles across tasks like VLN, searching, tracking, and driving.
- **State-of-the-art or competitive performance** on multiple navigation benchmarks without any task-specific fine-tuning.
- **Zero-shot generalization** to real-world environments, including unseen layouts and platforms.
- **Robustness** to varying camera configurations and navigation horizons.
- **Efficient inference** through dynamic token sampling under budget constraints.

## Relationships

- **Uses**: [[Vision-Language Models]] ⚠️ ⚠️ to interpret natural language instructions and visual observations.
- **Depends on**: The [[Identifier Tokens]] that encode embodiment and temporal context, and the [[Dynamic Sampling Strategy]] for efficient token selection.
- **Implements**: A unified architecture that can be applied to multiple [[Navigation]] ⚠️ paradigms.

## References

- Original paper: *NavFoM: Navigation Foundation Model for Cross-Embodiment and Cross-Task Navigation* (arXiv:2509.12129)