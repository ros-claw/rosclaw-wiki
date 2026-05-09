---
id: contrastive_language_image_pretraining_clip
title: Contrastive Language-Image Pretraining (CLIP)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:36:23'
last_reinforced: '2026-04-30T01:36:23'
supersedes: []
sources:
- papers/2302.06072.pdf
source_type: arxiv_paper
---

## Overview

**Contrastive Language-Image Pretraining (CLIP)** is a pre-trained vision-language model that learns visual concepts from natural language supervision. It is trained on a large corpus of image-text pairs using a contrastive loss, enabling it to perform zero-shot image classification and retrieve visual concepts from natural language descriptions. In the context of embodied intelligence, CLIP serves as a powerful feature extractor that bridges perception and semantic understanding.

## Capabilities

- Maps observations (e.g., camera images) to **actional atomic concept representations** – compact, semantic embeddings that can be used for high-level reasoning and task decomposition.
- Provides **object concept predictions**, allowing an agent to identify objects and their properties from visual input without task-specific fine-tuning.

## Relationships

- **Used by** → [[Actional Atomic-Concept Learning (AACL)]]: CLIP provides the visuo-semantic backbone that enables AACL to learn task-relevant semantics directly from demonstrations.

## References

- Radford, A., et al. "Learning Transferable Visual Models From Natural Language Supervision." *arXiv:2103.00020*, 2021.
- Source paper: *papers/2302.06072.pdf* (AACL) – builds upon CLIP.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Contrastive Language-Image Pretraining (CLIP)` --[[uses]] ⚠️--> `Actional Atomic-Concept Learning (AACL)`
