---
id: 3d_gaussian_splatting_3d_gs
title: 3D Gaussian Splatting (3D-GS)
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:44:12'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.15258.json
- papers/2512.15258.pdf
- papers/2508.00823.pdf
source_type: arxiv_paper
---

# 3D Gaussian Splatting (3D-GS)

## Overview

**3D Gaussian Splatting (3D-GS)** is a high‑fidelity scene representation and rendering algorithm that models a 3D scene as a collection of anisotropic Gaussian primitives. Originally developed for photorealistic novel‑view synthesis, it excels at **high‑fidelity scene reconstruction** and has been adapted for both **bridging the sim‑to‑real domain gap** in aerial navigation and as a core representation for **incremental scene building and goal localization** in image‑goal navigation.

The representation consists of **renderable 3D Gaussian primitives**, which are optimized **via differentiable rendering** to produce high‑quality novel view synthesis from sparse input views.

## Capabilities

- **High‑fidelity scene reconstruction** – 3D‑GS captures fine geometric and appearance details of complex scenes, enabling dense, realistic renderings from sparse input views.
- **High‑fidelity simulation data generation** – 3D‑GS can produce lifelike renderings of complex aerial scenes, which are used to train large vision‑language‑action (VLA) models without extensive real‑world data collection.
- **Domain adaptation from synthetic to real** – The algorithm’s ability to capture fine perceptual details reduces the visual gap between simulated and actual imagery, making policies learned in simulation transfer more reliably to physical quadrotors.
- **Supports novel view synthesis** – The differentiable Gaussian representation enables efficient rendering of arbitrary viewpoints from the optimized scene.

## Usage in the Knowledge Base

- **Implements**: domain adaptation techniques for aerial navigation; differentiable scene representation for image‑goal navigation.
- **Used by**: VLA-AN (aerial navigation), IGL-Nav (image‑goal navigation).
- **Depends on**: input data such as posed images or depth maps (typical for 3D Gaussian Splatting pipelines); these may be sourced from real drone flights, existing synthetic datasets, or robot exploration sequences.

### Role in VLA-AN

3D‑GS is used directly to construct a high‑fidelity dataset that effectively bridges the domain gap between training and real deployment. In the VLA-AN pipeline, 3D‑GS reconstructions of aerial environments serve as the primary source of photorealistic training data, enabling the VLA model to learn robust visual representations without requiring extensive real‑world flights.

### Role in IGL-Nav

In IGL-Nav (image‑goal navigation), 3D‑GS serves as the **core representation for incremental scene building and goal localization**. The robot builds a dynamic 3D Gaussian map of its environment on‑the‑fly during exploration, and the differentiable rendering of these Gaussians is used to localise the target goal image within the evolving scene representation. This allows IGL‑Nav to achieve robust navigation without prior maps.

## Related Concepts

- Sim‑to‑Real Transfer ⚠️
- Aerial Navigation ⚠️
- Domain Adaptation ⚠️
- Image‑Goal Navigation ⚠️
- IGL-Nav

---

*Sources:*  
- paper 2512.15258 – “VLA-AN: VLA with Aerial Navigation”  
- paper 2508.00823 – “IGL-Nav: Incremental 3D Gaussian Splatting for Image‑Goal Navigation”  

*See also: VLA-AN, IGL-Nav for details on how this algorithm is integrated.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `3D Gaussian Splatting (3D-GS)` --extends ⚠️ ⚠️--> `VLA-AN`  
- `3D Gaussian Splatting (3D-GS)` --extends ⚠️ ⚠️--> `IGL-Nav`