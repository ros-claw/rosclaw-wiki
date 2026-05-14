---
id: pre_training_and_fine_tuning_paradigm_for_vln
title: Pre-training and fine-tuning paradigm for VLN
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:17:35'
last_reinforced: '2026-04-29T21:17:35'
supersedes: []
sources:
- papers/2002.10638.pdf
source_type: arxiv_paper
---

## Pre-training and Fine-tuning Paradigm for VLN

A training paradigm for Vision-and-Language Navigation (VLN) ⚠️ ⚠️ that consists of pre-training a neural model on large-scale Image-Text-Action Triplets via Self-Supervised Learning, followed by fine-tuning on downstream VLN tasks. This approach provides generic representations of visual environments and language instructions, enabling effective learning on new VLN tasks with limited training data and improving generalization to unseen environments.

### Parameters

- **Training data**: Image-Text-Action Triplets
- **Learning method**: Self-Supervised Learning

### Capabilities

- Provides generic representations of visual environments and language instructions
- Enables effective learning on new VLN tasks with limited training data
- Improves generalization to unseen environments

### Relationships

- **Used by**: Prevalent VLN ⚠️ models
- **Applied to**: Vision-and-Language Navigation (VLN) ⚠️ ⚠️

### Demonstration

The paradigm has been successfully applied to several benchmarks, including Room-to-Room ⚠️ (R2R), Vision-and-Dialog Navigation (CVDN), and Help, Anna! ⚠️ tasks.