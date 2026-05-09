---
id: cot_vla
title: CoT-VLA
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T23:57:53'
last_reinforced: '2026-04-29T23:57:53'
supersedes: []
sources:
- papers/2601.13976.pdf
source_type: arxiv_paper
---

### CoT-VLA

**CoT-VLA** is a multimodal [[Chain-of-Thought]] ⚠️ (CoT) method designed for Vision-and-Language Navigation ([[Vision-Language Navigation|VLN]]). It generates intermediate visual observations as part of its reasoning process, intending to improve decision-making and grounding in unseen environments.

#### Parameters/Limitations

- **Type**: Multimodal Chain-of-Thought method.
- **Limitation**: CoT-VLA incurs severe **token inflation** by generating imagined visual observations. This overhead makes real-time navigation impractical, as it dramatically increases both computational cost and latency during inference.

#### Relationships

- **Part of**: [[Chain-of-Thought methods for VLN]] ⚠️.
- **Improved by**: [[FantasyVLN]] — a subsequent method that addresses the token inflation problem while preserving the benefits of visual CoT reasoning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CoT-VLA` --[[extends]] ⚠️--> `FantasyVLN`
