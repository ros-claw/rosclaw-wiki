---
id: cider
title: CIDEr
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:28:05'
last_reinforced: '2026-04-30T02:28:05'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

## CIDEr

**CIDEr** (Consensus-based Image Description Evaluation) is a metric originally designed to evaluate the quality of automatically generated image captions by measuring consensus among human reference captions. It uses TF-IDF weighting to emphasize informative n-grams and computes cosine similarity between candidate and reference caption vectors.

While CIDEr correlates well with human judgment in traditional [[Image Captioning]] ⚠️ tasks, it has been found **ineffective for [[Grounded Navigation Instructions]] ⚠️ ⚠️ evaluation** (source: `papers/2101.10504.pdf`). This is because grounded navigation instructions require spatial reasoning, action grounding, and alignment with a continuous environment — aspects that CIDEr’s n-gram overlap and consensus-based scoring do not capture.

### Relationships
- **ineffective_for**: [[Grounded Navigation Instructions]] ⚠️ ⚠️

### References
- `papers/2101.10504.pdf` — *"ET: Embodied Navigation Instruction Evaluation"* (or similar title)