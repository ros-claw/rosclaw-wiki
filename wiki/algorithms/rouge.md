---
id: rouge
title: ROUGE
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:26:03'
last_reinforced: '2026-04-30T02:26:03'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

# ROUGE

## Definition

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics originally developed for automatic evaluation of text summarization. It measures the overlap of n-grams, word sequences, or word pairs between a candidate text and one or more reference texts.

## Background

ROUGE was introduced by Lin & Hovy (2003) ⚠️ as a recall-based alternative to BLEU (precision-oriented). Common variants include ROUGE-N (n-gram overlap), ROUGE-L (longest common subsequence), ROUGE-W (weighted LCS), and ROUGE-S (skip-bigram co-occurrence). It has become a standard evaluation metric in Natural Language Processing ⚠️, particularly for summarization and generation tasks.

## Usage

ROUGE is typically applied to measure the quality of machine-generated summaries against human-written references. The recall score indicates what fraction of the reference content appears in the candidate, while F1 scores are often reported for balanced assessment.

## Limitations

### Ineffectiveness for Grounded Navigation Instructions Evaluation

ROUGE is known to correlate poorly with human judgment in tasks that require understanding of spatial, temporal, or referential grounding. Specifically, for Grounded Navigation Instructions Evaluation ⚠️ ⚠️, ROUGE fails to capture whether a generated instruction correctly guides an agent through an environment. The metric's reliance on surface form overlap cannot represent the correctness of action sequences, spatial relations, or object references that are critical in embodied tasks.

## Relations

- `ineffective_for` → Grounded Navigation Instructions Evaluation ⚠️ ⚠️  
- `used_in` → Text Summarization ⚠️ (automatic evaluation ⚠️)  
- `similar_to` → BLEU, METEOR, CIDEr

## See Also

- Evaluation Metrics ⚠️  
- Recall ⚠️  
- Natural Language Generation ⚠️