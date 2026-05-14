---
id: rxr
title: RxR
type: entity
tags:
- dataset
- vln
- multilingual
- matterport3d
confidence: 0.9
created_at: '2026-04-30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2010.07954.pdf
source_type: arxiv_paper
---

# RxR (Room-across-Room)

The **Room-across-Room (RxR)** dataset is a large-scale, multilingual Vision-and-Language Navigation (VLN) benchmark built on Matterport3D. It extends the VLN paradigm to multiple languages, enabling research on cross-lingual and multilingual embodied navigation.

## Parameters

- **Type**: Dataset
- **Task**: Vision-and-language navigation
- **Languages**: English, Hindi, Telugu
- **Environments**: Matterport3D indoor scans
- **Instructions**: ~126k natural language navigation instructions
- **Paths**: ~16k navigation paths
- **Annotators**: Native speakers of each language
- **Average instruction length**: ~55 words (English), comparable for other languages
- **Path length**: ~9.3m average geodesic distance

## Capabilities

- Train and evaluate VLN agents in a **multilingual setting**
- Study **cross-lingual transfer** for embodied navigation
- Benchmark **instruction-following robustness** across languages
- Evaluate **cultural and linguistic grounding** in navigation

## Relationships

- **Extends**: R2R — RxR uses the same Matterport3D environments as R2R but provides entirely new paths and multilingual instructions
- **Related dataset**: REVERIE — both use high-level natural language instructions, but REVERIE focuses on remote object grounding while RxR focuses on multilingual path following
- **Used by**: HAMT — HAMT demonstrates strong performance on RxR via hierarchical memory transformers
- **Evaluates**: Vision-Language Navigation — RxR is a core benchmark for this research area

## See Also

- Matterport3D ⚠️ — the underlying 3D environment dataset
- Vision-Language Navigation — the broader research field
- R2R — the original English-only VLN dataset
- Embodied AI — the field in which this dataset sits

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `RxR` --depends_on ⚠️ ⚠️--> `R2R`
- `RxR` --depends_on ⚠️ ⚠️--> `REVERIE`
- `RxR` --uses ⚠️--> `HAMT`
- `RxR` --related_to ⚠️ ⚠️--> `Vision-Language Navigation`
- `RxR` --related_to ⚠️ ⚠️--> `Embodied AI`
