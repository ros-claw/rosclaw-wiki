---
id: hm3d_dataset
title: HM3D dataset
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-30T00:13:28'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2502.19024.pdf
- papers/2312.03275.pdf
- code/PKU-SEC-Lab_EfficientNav/README.md
source_type: arxiv_paper
---

# HM3D Dataset

The **HM3D (Habitat-Matterport 3D Research Dataset)** is a large-scale, high-fidelity collection of 3D indoor spaces designed for training and evaluating embodied AI agents in realistic environments. It extends the earlier MP3D Dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ with a larger number of scenes and richer spatial structure, making it a foundational benchmark for navigation, exploration, and visual-language tasks.

## Description

The Habitat-Matterport 3D (HM3D) dataset is a collection of 3D indoor spaces used for training and evaluating navigation agents in `habitat-sim`. It provides photorealistic, semantically annotated reconstructions of real-world residences and commercial buildings, enabling effective sim-to-real transfer for embodied AI systems.

## Key Properties

- **Type**: 3D Indoor Scene Dataset ⚠️
- **Coverage**: Thousands of complex, fully-traversable indoor scenes with high-resolution textures, object semantics, and a connectivity graph.
- **Scope**: Released by the Habitat consortium as an open benchmark, HM3D improves upon its predecessor MP3D Dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ in scene diversity, scale, and annotation density.

## Capabilities

- Provides realistic 3D environments for navigation tasks including point-goal, object-goal, and exploration.
- Supports evaluation of open-vocabulary navigation, spatial reasoning, and sim-to-real transfer.

## Usage in Embodied AI

HM3D has been widely adopted to train and benchmark navigation policies, exploration algorithms, and visual-language models. Its high-fidelity geometry and semantics make it a standard testbed for embodied AI research.

- **Used by**: EfficientNav – the HM3D dataset is employed as the training and evaluation environment for the EfficientNav approach, which aims to improve navigation efficiency through spatial priors and hierarchical planning.
- **Used in evaluation of**: VLFM – the MP3D dataset served as one of the evaluation environments for the Vision-Language Frontier Maps (VLFM) approach; HM3D is the successor benchmark used in later studies.

## Relationship to MP3D

HM3D is the direct successor of the MP3D Dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ (Matterport3D). While MP3D contains hundreds of indoor scenes, HM3D expands to thousands and introduces a connectivity graph that encodes traversability between regions. Both datasets are supported by the Habitat Simulator, but HM3D is the preferred resource for modern embodied AI benchmarks due to its scale and structured spatial priors.

### 注意冲突

This page now describes the **HM3D Dataset** specifically. The earlier page content previously conflated properties of HM3D with those of MP3D. For the original MP3D details, see the separate MP3D Dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ page. The connectivity graph and thousands-of-scenes scale are properties of HM3D, not MP3D.

## Related

- MP3D Dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ (predecessor)
- Habitat Simulator
- Embodied AI Benchmark ⚠️
- Spatial Priors ⚠️ in Navigation
- VLFM
- EfficientNav

## Confidence

Initial confidence: 0.9 (source: official Habitat consortium documentation). Reinforced by additional source (README from EfficientNav repo) confirming HM3D as a `3D indoor scene dataset` and its use by EfficientNav.

### 自动链接关系
*These relationships were discovered automatically by the heuristic entity linker.*
**Confirmed links:**
- `HM3D dataset` —used_by ⚠️→ `EfficientNav`
- `HM3D dataset` —successor_of ⚠️→ `MP3D Dataset`
- `HM3D dataset` —type_of ⚠️→ `3D Indoor Scene Dataset`