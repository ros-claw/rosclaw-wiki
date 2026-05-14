---
id: self_supervised_learning
title: Self-supervised Learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:41:13'
last_reinforced: '2026-04-30T02:41:13'
supersedes: []
sources:
- papers/2002.10638.pdf
source_type: arxiv_paper
---

# Self-supervised Learning

**Self-supervised learning** is a pre-training method ⚠️ that learns useful representations from unlabelled data by designing pretext tasks that generate supervision from the data itself. In the context of embodied AI and visual navigation, self-supervised learning leverages large-scale **image-text-action triplets** to extract generic features without requiring manually annotated labels.

## Capabilities

- Learns representations without explicit labels, reducing dependency on costly human annotation.
- Can be used to pre-train models for downstream tasks such as Visual Language Navigation ⚠️ (VLN) and policy learning.

## Role in Prevalent

Prevalent employs self-supervised learning on large-scale visual and linguistic data to obtain generic embeddings. These embeddings transfer effectively to new navigation tasks, enabling the model to handle unseen environments and linguistic instructions without task-specific fine-tuning.

## Relationship to VLN

Self-supervised learning enables the creation of **generic representations for VLN** by aligning visual features with linguistic concepts and action sequences. This approach helps bridge the gap between simulation and real-world deployment, as the learned representations capture reusable patterns from diverse multimodal data.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Self-supervised Learning` --applies_to ⚠️--> `Prevalent`
