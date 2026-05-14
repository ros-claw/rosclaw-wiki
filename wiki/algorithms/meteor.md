---
id: meteor
title: METEOR
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:27:07'
last_reinforced: '2026-04-30T02:27:07'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

# METEOR

**METEOR** is an automatic metric for evaluating the quality of generated navigation instructions in grounded navigation tasks. It was introduced in the paper "METEOR: An Automatic Metric for Evaluating Grounded Navigation Instructions" (arXiv:2101.10504). METEOR aligns with human judgments more closely than traditional lexical overlap metrics by incorporating semantic matching and entity grounding.

## Key Findings

Despite its design purpose, empirical evaluation reveals that METEOR demonstrates poor correlation with human assessments when applied to **grounded navigation instructions evaluation**. The metric fails to capture key aspects of instruction quality, such as spatial grounding and actionability, making it **ineffective** for this specific application.

## Relationships

- `ineffective_for` :: Grounded Navigation Instructions Evaluation ⚠️ – METEOR does not reliably assess instructions in grounded navigation contexts.
- `depends_on` :: Semantic Similarity Metrics ⚠️ – Uses token-level semantic matching.
- `related_to` :: BLEU, ROUGE – Shares lineage with n-gram-based metrics but adds grounding.

## Usage Notes

METEOR should not be used as a primary metric for evaluating embodied instruction generation without significant adaptation. Alternative metrics like Task Success Rate ⚠️ or Human Likert Ratings ⚠️ are more appropriate for grounded settings.

---

*Source: arXiv:2101.10504*