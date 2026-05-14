---
id: masked_panorama_modeling
title: Masked Panorama Modeling
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:49:36'
last_reinforced: '2026-04-30T01:49:36'
supersedes: []
sources:
- papers/2304.04907.pdf
source_type: arxiv_paper
---

# Masked Panorama Modeling

**Masked Panorama Modeling (MPM)** is a proxy pre-training task designed to teach an agent spatial awareness by predicting masked portions of a panoramic view. It is a self-supervised objective where the model must complete missing views given the visible context, simulating the agent’s ability to anticipate unseen surroundings.

## Overview

In MPM, the input is a panorama ⚠️ with certain views masked out; the output is the predicted missing views. By learning to infer occluded or unobserved regions, the model develops a representation of the environment that supports navigation and scene understanding tasks. This technique is particularly effective in in-domain pre-training for Vision-and-Language Navigation (VLN), where spatial reasoning is critical.

## Parameters

- **Task type**: Proxy pre-training task
- **Input**: Panorama with masked views
- **Output**: Predicted missing views

## Capabilities

- Models the agent’s ability to predict missing views in a panorama
- Learns spatial continuity and layout priors from panoramic data
- Provides a self-supervised signal that reduces reliance on expensive annotations

## Relationships

- **Part of**: VLN-SIG
- **Used in**: in-domain pre-training ⚠️

MPM is a component of the VLN-SIG framework, where it serves as one of several proxy tasks during the in-domain pre-training phase.

## See Also

- Panoramic Image Completion ⚠️
- Self-Supervised Learning for Navigation ⚠️
- Masked Autoencoder for Visual Data ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Masked Panorama Modeling` --based_on ⚠️--> `Vision-and-Language Navigation`
