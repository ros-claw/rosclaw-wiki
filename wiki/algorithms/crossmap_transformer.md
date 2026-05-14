---
id: crossmap_transformer
title: CrossMap Transformer
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:12:44'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2103.00852.pdf
source_type: arxiv_paper
---

## CrossMap Transformer

The **CrossMap Transformer** is a crossmodal masked path Transformer that uses double back‑translation for Vision-and-Language Navigation (VLN) ⚠️ ⚠️. It predicts a sequence of actions given natural-language navigation instructions while jointly learning to generate both paths and instructions. The core innovation is a double back‑translation loop that mutually enhances path generation and instruction generation via shared latent features.

---

### Overview

CrossMap Transformer is a crossmodal masked path Transformer that uses double back‑translation for vision-and-language navigation. It predicts a sequence of actions given natural language navigation instructions and jointly learns to generate paths and instructions using a double back‑translation mechanism, where generated paths are translated into instructions and vice versa, with shared latent features.

### Architecture

- **Type**: Transformer-based
- **Components**:
  - **Encoder** for linguistic and visual features
  - **Path generator**
  - **Double back‑translation loop** (comprising a Transformer ⚠️ ⚠️-based speaker and a separate instruction generator)

### Capabilities

- Predicts a sequence of actions for navigation.
- Generates navigation instructions from observed visual context.
- Encodes linguistic and visual features to sequentially generate a navigation path.
- Mutual enhancement between path generation and instruction generation via double back‑translation.

### Relationships

- **Uses**:
  - Transformer ⚠️ ⚠️
  - Double Back Translation
  - Transformer-based Speaker
- **Depends on**:
  - Vision-and-Language Navigation (VLN) ⚠️ ⚠️
- **Part of**:
  - *(none listed)*

### Source

- Paper: [*CrossMap Transformer: A Transformer-based Cross-modal Mapping for Vision-and-Language Navigation*](papers/2103.00852.pdf) (2021).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CrossMap Transformer` --extends ⚠️--> `Double Back Translation`