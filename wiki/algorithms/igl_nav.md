---
id: igl_nav
title: IGL-Nav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:52:27'
last_reinforced: '2026-04-30T03:52:27'
supersedes: []
sources:
- papers/2508.00823.pdf
source_type: arxiv_paper
---

# IGL-Nav

## Overview

**IGL-Nav** is an **incremental 3D Gaussian localization framework** for [[Image-Goal Navigation]]. It incrementally builds and updates a [[3D Gaussian Splatting (3DGS)]] ⚠️ ⚠️ scene representation from monocular RGB input, enabling **efficient goal localization** and **free-view image-goal navigation**.

The framework operates in two stages:

1. **Coarse discrete matching** — a 3D convolution‑equivalent step that matches the current observation to the Gaussian representation.
2. **Fine pose optimization** — via differentiable rendering, refining the location estimate against the goal image.

This approach allows **real‑world deployment** with goal images captured by a cellphone, without prior scene knowledge.

## Parameters

| Parameter | Value |
|-----------|-------|
| Representation | incremental 3D Gaussian |
| Localization | coarse discrete matching → fine pose optimization |
| Scene update | feed-forward monocular prediction |

## Capabilities

- Efficient image-goal navigation in large scenes
- 3D-aware goal localization without dense maps
- Free-view image-goal setting (goal can be taken from any viewpoint)
- Real-world deployment with cellphone-captured goal images

## Relationships

- **uses** → [[3D Gaussian Splatting (3DGS)]] ⚠️ ⚠️, [[Differentiable Rendering]] ⚠️, [[Monocular Prediction]] ⚠️
- **depends_on** → [[3DGS optimization]] ⚠️
- **improves_upon** → prior end-to-end RL policies and modular-based policies using topological graphs or [[Bird’s Eye View (BEV)]] ⚠️ representations

## Source

Derived from the paper *IGL-Nav: Incremental Gaussian Localization for Image-Goal Navigation* (arXiv:2508.00823, 2025).