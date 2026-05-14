---
id: multitask_learning_for_vln_rxr_r2r
title: Multitask Learning for VLN (RxR + R2R)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:06:21'
last_reinforced: '2026-04-30T03:06:21'
supersedes: []
sources:
- papers/2010.07954.pdf
source_type: arxiv_paper
---

# Multitask Learning for VLN (RxR + R2R)

**Multitask Learning for VLN** is an algorithm that jointly trains a Vision-and-Language Navigation (VLN) model on multiple annotated datasets, specifically Room-Across-Room (RxR) and Room-to-Room (R2R), to learn shared representations that improve navigation performance over single-dataset training. The approach supports both monolingual and multilingual settings.

## Parameters

- **Tasks**: Room-Across-Room (RxR), Room-to-Room (R2R)
- **Setting**: Monolingual and multilingual

## Capabilities

- Improves navigation performance by learning shared representations across datasets

## Relationships

- **Depends on**: Room-Across-Room (RxR), Room-to-Room (R2R)

## Description

Baseline results from this multitask learning approach combine RxR and R2R annotations, demonstrating significant improvements over models trained on a single dataset. By leveraging complementary visual and linguistic patterns in both datasets, the algorithm learns more robust navigation policies that generalize better across environments and instructions.

## References

- *Multitask Learning for VLN* (arXiv:2010.07954) – source paper for this algorithm.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multitask Learning for VLN (RxR + R2R)` --based_on ⚠️--> `Room-Across-Room (RxR)`
