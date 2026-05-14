---
id: self_reflective_post_training
title: Self-Reflective Post-Training
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T01:04:26'
last_reinforced: '2026-04-30T01:04:26'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

# Self-Reflective Post-Training

**Self-Reflective Post-Training** is a second-stage, iterative skill that enhances a model's reasoning by leveraging its own outputs in a Self-Reflective auxiliary task. It builds upon Formalized CoT Supervised Fine-Tuning to improve reasoning diversity and correctness. This skill is a core component of the EvolveNav framework.

## Key Characteristics

- **Stage**: Second (post‑SFT)
- **Iterative**: Yes
- **Self‑Reflective Auxiliary Task**: Yes

## Capabilities

- **Enhances supervision diversity** by enriching Chain-of-Thought ⚠️ (CoT) labels using the model's own generated reasoning paths.
- **Encourages learning correct reasoning patterns** by contrasting them with incorrect ones (e.g., via contrastive learning or self‑critique).

## Relationships

- **part_of**: EvolveNav
- **uses**: The model’s own reasoning outputs, Self-Reflective auxiliary task
- **depends_on**: Formalized CoT Supervised Fine-Tuning

## Source

This page is based on the paper *2506.01551.pdf* (arXiv).

---

*Last reinforced: YYYY-MM-DD | Confidence: 0.8 (peer-reviewed paper)*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Self-Reflective Post-Training` --uses ⚠️--> `EvolveNav`
