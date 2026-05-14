---
id: lavira
title: LaViRA
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:05'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.19655.pdf
source_type: arxiv_paper
---

# LaViRA

**LaViRA** (Language-Vision-Robot Action) is a zero-shot framework for **Vision-and-Language Navigation (VLN) ⚠️ ⚠️ in Continuous Environments**. It decomposes robotic navigation into a coarse-to-fine action hierarchy, leveraging the distinct strengths of Multimodal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️ at different scales. The framework achieves state-of-the-art performance on the VLN-CE benchmark while maintaining transparency and suitability for real-world deployment.

## Parameters

| Parameter   | Value        |
|-------------|--------------|
| Framework   | Zero-shot    |
| Hierarchy   | Coarse-to-fine |
| Decomposition | Language Action → Vision Action → Robot Action |

## Architecture

LaViRA decomposes navigation into three stages, following a coarse-to-fine progression:

1. **Language Action** – High-level planning using large-scale MLLMs to interpret natural language instructions and generate abstract route plans.
2. **Vision Action** – Middle-level perceptual grounding, aligning visual observations with the language plan using mid-scale MLLMs.
3. **Robot Action** – Low-level control executed by small-scale MLLMs or classical controllers, translating the grounded plan into motor commands.

This staged design allows each level to operate at an appropriate scale of model complexity, balancing reasoning power with computational efficiency.

## Capabilities

- **Zero-shot Vision-and-Language Navigation** in continuous, unseen environments – no task-specific training or environment-specific waypoint predictors are required.
- **State-of-the-art performance** on the VLN-CE benchmark, outperforming existing zero-shot methods.
- **Superior generalization** in unseen environments without additional adaptation.
- **Transparency and efficiency** designed for real-world deployment, with interpretable intermediate representations at each hierarchy level.

## Performance

LaViRA significantly outperforms existing zero-shot approaches on the VLN-CE benchmark, demonstrating strong generalization even without environment-specific waypoint predictors. Its coarse-to-fine action hierarchy enables robust navigation across diverse, previously unseen settings.

## Relationships

- **Uses**: Multimodal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️ (at multiple scales) – LaViRA relies on MLLMs for language understanding, visual grounding, and control policy generation.
- **Depends on**: VLN-CE benchmark for evaluation; Multimodal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️ as core reasoning engines.
- **Implements**: A zero-shot Vision-and-Language Navigation (VLN) ⚠️ ⚠️ framework, built on zero-shot learning principles – no training is required for new environments.

## Source

- Paper: *LaViRA: A Zero-Shot Framework for Vision-and-Language Navigation in Continuous Environments* – arXiv: 2510.19655 (2025).