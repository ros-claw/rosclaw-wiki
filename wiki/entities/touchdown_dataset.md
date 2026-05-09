---
id: touchdown_dataset
title: Touchdown dataset
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:01:36'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2402.03561.pdf
source_type: arxiv_paper
---

## Touchdown dataset

**Touchdown** is a standard benchmark dataset for outdoor **[Vision-and-Language Navigation (VLN)]**, consisting of routes collected in urban environments (primarily U.S. cities such as New York) annotated with natural language instructions. It serves as both a pretraining and fine-tuning resource for VLN models and as the primary evaluation benchmark for methods like [[VLN-Video]].

### Domain

Outdoor navigation — the dataset focuses on real‑world street‑level trajectories requiring cross‑view and temporal reasoning.

### Capabilities

- Provides a challenging **outdoor VLN benchmark** with human‑written instructions and corresponding routes.
- Supports **pretraining and fine-tuning** of VLN models, enabling both large‑scale representation learning and task‑specific adaptation.
- Enables comparison against previous outdoor VLN methods and serves as a reference for new approaches.

### Usage

Touchdown is commonly used in **pretraining** to learn strong visual‑language representations from grounded navigation data, followed by **fine-tuning** on the same dataset's evaluation splits. This two‑stage pipeline is employed by state‑of‑the‑art models such as [[VLN-Video]].

### Relationships

- **Used by:** [[VLN-Video]] and numerous prior outdoor VLN methods as a primary evaluation set.
- **Depends on:** Real‑world street‑level imagery and GPS traces for trajectory generation.
- **Related to:** Other outdoor VLN datasets (e.g., [[StreetLearn]] ⚠️) and indoor datasets like [[R2R]].

### See also

- [[Vision-and-Language Navigation]]
- [[VLN-Video]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Touchdown dataset` --[[uses]] ⚠️--> `VLN-Video`