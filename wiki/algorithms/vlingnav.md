---
id: vlingnav
title: VLingNav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:41:43'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2601.08665.pdf
source_type: arxiv_paper
---

## Overview

**VLingNav** is a Vision-Language-Action (VLA) model for **embodied navigation grounded in linguistic-driven cognition**. It integrates adaptive Chain-of-Thought (CoT) reasoning with a cross-modal memory module, enabling robots to handle long-horizon spatial dependencies and generalize zero-shot to unseen environments. VLingNav is trained via supervised fine-tuning and online expert-guided reinforcement learning on the largest embodied navigation dataset with reasoning annotations.

## Capabilities

- **Adaptive reasoning** – dynamically triggers explicit reasoning when necessary, fluidly switching between fast intuitive execution (System 1) and slow deliberate planning (System 2).
- **Long-term spatial memory** – via Visual-assisted Linguistic Memory ⚠️ ⚠️ ⚠️ which stores and retrieves cross-modal semantic associations across time.
- **Zero-shot transfer** to real-world robotic platforms without platform-specific retraining.
- **State-of-the-art performance** across multiple embodied navigation benchmarks.
- **Cross-domain and cross-task generalization** – performs reliably across diverse environments and instruction types.

## Architecture

VLingNav implements the **Dual-process theory**, combining fast intuitive perception (System 1) with deliberate, Chain-of-Thought reasoning (System 2). Its two core components are:

- **Adaptive Chain-of-Thought (AdaCoT) ⚠️ ⚠️** – a reasoning module that dynamically invokes CoT steps when uncertainty or ambiguity is detected, reducing unnecessary computation in simple cases.
- **Visual-assisted Linguistic Memory ⚠️ ⚠️ ⚠️** – a cross-modal memory that encodes spatial observations as linguistically grounded representations, enabling the model to recall and reason over past visual context during navigation.

## Training

VLingNav is trained in two stages:

1. **Supervised Fine-Tuning (SFT)** on the Nav-AdaCoT-2.9M dataset, which consists of 2.9 million navigation episodes with detailed step-by-step reasoning annotations.
2. **Online Expert-Guided Reinforcement Learning (RL)** – an expert policy provides corrective feedback during training, refining the model's action selection and reasoning quality.

## Performance

VLingNav achieves **state-of-the-art results** on standard embodied navigation benchmarks and demonstrates robust **zero-shot generalization** to real-world robotic platforms, requiring no platform-specific retraining.

## Dependencies & Relationships

| Relationship | Entity |
|--------------|--------|
| **uses** | Adaptive Chain-of-Thought (AdaCoT) ⚠️ ⚠️ |
| **uses** | Visual-assisted Linguistic Memory ⚠️ ⚠️ ⚠️ |
| **uses** | Online Expert-Guided RL ⚠️ |
| **depends_on** | Nav-AdaCoT-2.9M |
| **depends_on** | Dual-process theory |
| **depends_on** | Linguistic-driven Cognition ⚠️ |

## Summary

VLingNav is a VLA model that integrates adaptive CoT reasoning and a cross-modal memory module, trained with supervised fine-tuning and online expert-guided reinforcement learning on the largest embodied navigation dataset with reasoning annotations. Grounded in linguistic-driven cognition, its design enables state-of-the-art benchmark performance, robust zero-shot transfer, and efficient long-horizon planning, making it a strong candidate for real-world robotic navigation tasks.