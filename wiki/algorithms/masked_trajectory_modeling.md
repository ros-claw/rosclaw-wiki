---
id: masked_trajectory_modeling
title: Masked Trajectory Modeling
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:50:14'
last_reinforced: '2026-04-30T01:50:14'
supersedes: []
sources:
- papers/2304.04907.pdf
source_type: arxiv_paper
---

### Masked Trajectory Modeling

**Masked Trajectory Modeling (MTM)** is a proxy pre-training task designed for the **[[VLN-SIG]]** framework. It operates by randomly masking intermediate steps in a full navigation trajectory and training the model to reconstruct those missing steps. This forces the model to learn the underlying structure and dynamics of navigation sequences, improving its ability to generalize across unseen environments.

#### Description

Masked Trajectory Modeling (MTM) is a proxy task that masks intermediate steps in a navigation trajectory and requires the model to reconstruct them. By doing so, MTM encourages the model to capture temporal dependencies and spatial reasoning needed for coherent path completion. It is analogous to masked language modeling in NLP, but applied to sequences of visual observations and actions.

#### Parameters

| Parameter | Value |
|-----------|-------|
| **Task type** | Proxy pre-training task |
| **Input** | Partial trajectory (missing steps) |
| **Output** | Predicted missing steps |

#### Capabilities

- Teaches the model to predict missing steps in the full trajectory, thereby learning the sequential structure of navigation.
- Enhances the model's ability to reason about intermediate positions and actions, which is critical for **[[Visual Language Navigation]] ⚠️**.
- Serves as a self-supervised signal during in-domain pre-training, bootstrapping more generalizable representations.

#### Relationships

- **Part of** → [[VLN-SIG]]  
- **Used in** → [[in-domain pre-training]] ⚠️ (within VLN-SIG)  
- **Related to** → [[Masked Language Modeling]] ⚠️, [[Masked Autoencoding]] ⚠️ – shares the masked reconstruction principle
- **Depends on** → [[Partial Trajectory Sampling]] ⚠️, [[Tokenization for Navigation Sequences]] ⚠️