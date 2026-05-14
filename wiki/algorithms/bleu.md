---
id: bleu
title: BLEU
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:25:20'
last_reinforced: '2026-04-30T02:25:20'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

# BLEU

**BLEU** (Bilingual Evaluation Understudy) is an algorithm for evaluating the quality of machine-generated text, originally developed for Machine Translation ⚠️. It measures n-gram overlap between a candidate text and one or more reference texts, producing a score between 0 and 1 (or 0–100). BLEU is widely used in Natural Language Processing ⚠️ tasks such as Text Generation ⚠️, Summarization ⚠️, and Image Captioning ⚠️.

## Algorithm Overview

BLEU computes precision of n-grams (typically unigrams through 4-grams) in the candidate text compared to the reference texts, with a brevity penalty to discourage overly short outputs. The final score is the geometric mean of n-gram precisions multiplied by the brevity penalty.

## Limitations

Despite its popularity, BLEU has well-known weaknesses: it does not capture semantic meaning, fluency, or factual correctness. It also depends heavily on the quality and number of reference texts.

### Ineffective for Grounded Navigation Instructions Evaluation

According to recent analysis in arxiv:2101.10504 ⚠️, BLEU is **ineffective** for evaluating grounded navigation instructions. In tasks like Embodied Navigation or Vision-and-Language Navigation (VLN) ⚠️, the generated instructions must be validated against physical environments or spatial constraints, which BLEU’s purely lexical overlap metric cannot capture. This finding reinforces the need for task-specific evaluation metrics in Embodied AI.

## Relationship Annotations

- `ineffective_for` → Grounded Navigation Instructions Evaluation ⚠️
- `depends_on` → N-gram Overlap Metrics ⚠️
- `used_in` → Machine Translation Evaluation ⚠️
- `replaced_by` (in many contexts) → BERTScore ⚠️, METEOR, CIDEr, SPICE

## See Also

- Evaluation Metrics in NLP ⚠️
- Grounded Language Learning ⚠️
- Sim-to-Real Transfer

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `BLEU` --based_on ⚠️--> `Embodied AI`
