---
id: closed_loop_feedback_with_confidence_scores
title: Closed-Loop Feedback with Confidence Scores
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:40:42'
last_reinforced: '2026-04-29T20:40:42'
supersedes: []
sources:
- papers/2504.09000.pdf
source_type: arxiv_paper
---

### Closed-Loop Feedback with Confidence Scores

**Closed-Loop Feedback with Confidence Scores** is a concept within the [[CL-CoTNav]] framework that leverages detection and reasoning confidence scores as dynamic feedback signals to improve training and inference robustness. By adaptively weighting data pairs based on their confidence, the approach mitigates the impact of noisy inputs and enhances resilience against hallucinated or incorrect reasoning.

#### Parameters

- **Feedback signal**: detection and reasoning confidence scores
- **Integration**: adaptive weighting in training to prioritize high-confidence data pairs

#### Capabilities

- Mitigates impact of noisy inputs
- Enhances robustness against hallucinated or incorrect reasoning

#### Relationships

- `part_of` → [[CL-CoTNav]]
- `depends_on` → [[Confidence Score]] ⚠️, [[Adaptive Weighting]] ⚠️
- `uses` → [[Detection Model]] ⚠️, [[Reasoning Module]] ⚠️ (indirectly, via the confidence scores they produce)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Closed-Loop Feedback with Confidence Scores` --[[related_to]] ⚠️--> `CL-CoTNav` _(wikilink)_
