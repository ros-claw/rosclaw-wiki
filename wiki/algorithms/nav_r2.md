---
id: nav_r2
title: Nav-R^2
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:47:53'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02400.pdf
source_type: arxiv_paper
---

## Nav-R^2

Nav-R^2 is a framework that explicitly models two critical types of relationships — **target-environment modeling** and **environment-action planning** — through structured Chain-of-Thought (CoT) reasoning coupled with a Similarity-Aware Memory (SA-Mem). This dual-relation approach achieves state-of-the-art performance in generalizable **open-vocabulary object-goal navigation**, localizing unseen objects in unseen environments without overfitting to seen categories, while maintaining real-time inference at **2 Hz**.

### Capabilities

- Localizing unseen objects in open-vocabulary settings
- Generalization to unseen environments without retraining
- State-of-the-art performance in open-vocabulary object-goal navigation
- Real-time inference at **2 Hz**
- Avoids overfitting to seen object categories

### Technical Details

The framework operates at a **2 Hz** inference rate. It uses a Similarity-Aware Memory (SA-Mem) that compresses video frames and fuses historical observations from both temporal and semantic perspectives without adding extra parameters. The Chain-of-Thought ⚠️ component, realized through **dual-relation reasoning**, teaches the model to perceive the environment, focus on target-related objects, and make action plans by explicitly modeling target–environment and environment–action relationships.

### Relationships

- **uses** → Chain-of-Thought (CoT) reasoning
- **uses** → Similarity-Aware Memory (SA-Mem)
- **depends_on** → NavR^2-CoT dataset

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Nav-R^2` --based_on ⚠️--> `Chain-of-Thought reasoning`