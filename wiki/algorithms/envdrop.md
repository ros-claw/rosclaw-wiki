---
id: envdrop
title: EnvDrop
type: algorithm
tags:
- vln
- data-augmentation
- reinforcement-learning
- r2r
confidence: 0.85
created_at: '2026-04-30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1904.04195.pdf
source_type: arxiv_paper
---

# EnvDrop (Environment Dropout)

**EnvDrop** is a data augmentation technique for Vision-and-Language Navigation that improves agent generalization by randomly masking visual features during training. It was introduced as a simple yet effective regularization method for VLN agents operating in discrete environments like Matterport3D.

## Parameters

- **Type**: Data augmentation / regularization technique
- **Task**: Vision-and-language navigation
- **Dropout rate**: Typically 0.3–0.5 for visual features
- **Applied to**: Panoramic image features (36 views per node)
- **Training paradigm**: Reinforcement learning with imitation learning pre-training
- **Environments**: Matterport3D (discrete graph)
- **Datasets**: [[R2R]], [[RxR]]

## Method

EnvDrop applies dropout directly to the visual observation encoder's output features. During each training step, a random subset of the 36 discrete view angles is masked (set to zero), forcing the agent to navigate even when some visual information is missing. This:

1. **Reduces overfitting** to specific visual patterns
2. **Improves robustness** to partial observations
3. **Encourages language grounding** — the agent must rely more heavily on textual instructions

## Capabilities

- Improve generalization from seen to unseen environments
- Reduce performance gap between training and validation splits
- Compatible with most VLN architectures as a drop-in regularizer

## Relationships

- **Improves**: [[Speaker-Follower]] — EnvDrop is commonly combined with the speaker-follower framework for better results
- **Used on**: [[R2R]] — primary benchmark for evaluation
- **Related to**: [[Self-Monitoring]] ⚠️ — both are regularization techniques for VLN
- **Precedes**: [[AuxRN]] ⚠️ — later methods build on the intuition that visual dropout helps language grounding

## See Also

- [[Vision-Language Navigation]] — the broader field
- [[Data Augmentation]] ⚠️ — general techniques for embodied AI
- [[R2R]] — the primary benchmark dataset

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EnvDrop` --[[implements]] ⚠️ ⚠️--> `R2R`
- `EnvDrop` --[[implements]] ⚠️ ⚠️--> `RxR`
- `EnvDrop` --[[extends]] ⚠️--> `Speaker-Follower`
- `EnvDrop` --[[based_on]] ⚠️--> `Vision-Language Navigation`
