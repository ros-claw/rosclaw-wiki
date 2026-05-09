---
id: huron
title: HuRoN
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:32:55'
last_reinforced: '2026-04-29T21:32:55'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

### HuRoN

**HuRoN** is a benchmark for visual navigation, specifically designed to evaluate the performance of embodied navigation agents. It was used as a test environment in the evaluation of [[UniWM]].

#### Relationships

- **part_of**: [[Navigation benchmarks]] ⚠️
- **depends_on**: Visual navigation tasks and datasets (implicit)
- **used_by**: [[UniWM]] for evaluation

#### Description

HuRoN provides a standardized suite of visual navigation challenges, enabling fair comparison between different navigation algorithms and models. Its inclusion in the UniWM study highlights its role in assessing generalist visual navigation agents across diverse environments. The benchmark likely includes multiple episodes, scenes, and metrics for measuring navigation success, efficiency, and generalization.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HuRoN` --[[uses]] ⚠️--> `UniWM`
