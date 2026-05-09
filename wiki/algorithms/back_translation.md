---
id: back_translation
title: Back Translation
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:05:11'
last_reinforced: '2026-04-30T03:05:11'
supersedes: []
sources:
- papers/1904.04195.pdf
source_type: arxiv_paper
---

## Back Translation

**Back Translation** is a semi-supervised learning technique designed to improve the generalizability of navigational agents. It works by generating new paths and corresponding instructions from unlabeled trajectory data, effectively expanding the training distribution without requiring additional human annotations.

The method is particularly effective when combined with [[Environmental Dropout]] — a technique that creates diverse visual variations of the environment — and is a key component of the [[Generalizable Navigational Agent]] framework.

### Capabilities

- Generate new paths and instructions from unlabeled data.
- Enable semi-supervised learning for navigation tasks, reducing reliance on expensive human annotation.

### Relationships

- **Depends on** [[Environmental Dropout]] for creating the visual perturbations used in the back‑translation pipeline.
- **Used in** [[Generalizable Navigational Agent]] to enhance the agent’s ability to generalize across unseen environments.

### Source

- arXive paper: *Generalization Through Hand‑Eyes Coordination in Deep Reinforcement Learning* (1904.04195)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Back Translation` --[[extends]] ⚠️--> `Environmental Dropout`
