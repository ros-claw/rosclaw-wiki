---
id: vlfm
title: VLFM
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:13:14'
last_reinforced: '2026-04-30T04:13:14'
supersedes: []
sources:
- papers/2312.03275.pdf
source_type: arxiv_paper
---

# VLFM

**VLFM (Value‑Leveraged Frontier Mapping)** is a zero‑shot semantic navigation algorithm that locates instances of a target object category using only RGB‑D observations and a pre‑trained vision‑language model. It was introduced in the paper "Value‑Leveraged Frontier Mapping for Zero‑Shot Object Navigation" (arXiv 2312.03275).

## Description

VLFM builds Occupancy maps ⚠️ ⚠️ from depth observations to identify frontiers (boundaries between explored and unexplored space). RGB observations are passed through a Pre-trained vision-language model to generate a *language‑grounded value map*, which scores each frontier according to how likely it is to lead to an instance of the given target category. The robot then selects and traverses to the most promising frontier, repeating the cycle until the object is found or all frontiers are exhausted.

## Capabilities

- **Zero‑shot semantic navigation** to unseen objects — no task‑specific fine‑tuning is required.
- Achieves **state‑of‑the‑art SPL** (Success weighted by Path Length) on the Gibson ⚠️, HM3D, and MP3D benchmark datasets.
- Successfully deployed in the real world on a Boston Dynamics Spot robot.

## Parameters

| Parameter            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `input_observations` | Depth + RGB (from an RGB-D camera ⚠️ ⚠️)                                      |
| `output`             | Language‑grounded value map (scores frontiers by relevance to target)       |
| `target_category`    | A string specifying the object class to find (e.g., "chair", "couch")       |

## Relationships

- **Uses** → Occupancy maps ⚠️ ⚠️, Pre-trained vision-language model, Frontier-based exploration
- **Depends on** → Habitat simulator (for training and evaluation), RGB-D camera ⚠️ ⚠️ (for real‑world deployment)
- **Part of** → Zero‑shot object navigation research pipeline in embodied AI

## References

- VLFM Paper: arXiv 2312.03275 (2023)
- Implementation evaluated in Habitat benchmark environments (Gibson, HM3D, MP3D)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLFM` --implements ⚠️--> `Boston Dynamics Spot`
