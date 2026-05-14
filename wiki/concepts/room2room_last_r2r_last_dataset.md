---
id: room2room_last_r2r_last_dataset
title: Room2Room Last (R2R-Last) Dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:05:42'
last_reinforced: '2026-04-30T02:05:42'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

# Room2Room Last (R2R-Last) Dataset

**Type**: Concept  
**Tags**: dataset, benchmark, vision-and-language navigation  
**Confidence**: 0.8 (derived from peer-reviewed paper)  
**Sources**: `papers/2302.09230.pdf`

## Overview

The **Room2Room Last (R2R-Last) Dataset** is a variant of the original Room-to-Room (R2R) Dataset that specifically focuses on the **last step** of navigation instructions. It is designed to test and benchmark models that must predict the final action or location given a partial trajectory and incomplete language instruction. The dataset isolates the critical decision at the end of a navigation episode, making it a targeted probe for *task completion* in Vision and Language Navigation Benchmarks ⚠️ ⚠️.

## Description

R2R-Last strips down the standard R2R evaluation to the terminal segment of each path. Instructions are truncated to only describe the final leg, and agents are only evaluated on whether they correctly reach the goal from the penultimate viewpoint. This variant is used to measure an agent’s ability to process last-step language and execute precise spatial action, without the confounding influence of earlier navigation errors. The dataset is derived from the same Matterport3D environments as the full R2R.

## Relationships

- **`used_by`**: VLN-Trans Evaluation ⚠️ — the dataset serves as a primary benchmark for evaluating the VLN-Trans model's performance on last-step inference.
- **`part_of`**: Vision and Language Navigation Benchmarks ⚠️ ⚠️ — R2R-Last is one of several focused benchmarks (alongside R2R, R4R, etc.) that collectively assess different aspects of vision-and-language navigation.

## Usage Notes

Because R2R-Last isolates the final decision, it is especially sensitive to a model’s *local grounding* and *instruction following* at the last moment. Success on this benchmark does not guarantee robust long-horizon navigation, but failure indicates a clear weakness in closing the loop with language. When reporting results, researchers typically cite both full R2R and R2R-Last scores.

## References

- Original R2R Dataset: `data/raw/r2r_dataset.md` (if available)
- VLN-Trans paper: `papers/2302.09230.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room2Room Last (R2R-Last) Dataset` --applies_to ⚠️--> `Room-to-Room (R2R) Dataset`
