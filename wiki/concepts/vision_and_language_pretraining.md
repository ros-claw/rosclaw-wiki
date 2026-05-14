---
id: vision_and_language_pretraining
title: Vision-and-Language Pretraining
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:26:48'
last_reinforced: '2026-04-30T02:26:48'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

## Vision-and-Language Pretraining

**Vision-and-Language Pretraining (VLP)** is a concept in embodied AI and vision-language navigation (VLN). It refers to a pretraining approach that learns an alignment between visual and textual representations from large-scale web data. The learned representations are subsequently fine-tuned for downstream tasks such as the Room-to-Room ⚠️ (R2R) and Room-across-Room ⚠️ (RxR) benchmarks.

VLP is a foundational technique that substantially improves performance on the R2R and RxR benchmarks. It is used by the Scene- and Object-Aware Transformer (SOAT) model, which builds on VLP to incorporate scene- and object-level context.

The concept depends on large-scale web data and serves the purpose of learning cross-modal alignment. VLP is a typical example of transfer learning ⚠️ applied to Vision-Language Navigation.

### Relationships

- **used\_by**: Scene- and Object-Aware Transformer (SOAT)