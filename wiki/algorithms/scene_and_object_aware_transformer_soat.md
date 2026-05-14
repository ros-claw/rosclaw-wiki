---
id: scene_and_object_aware_transformer_soat
title: Scene- and Object-Aware Transformer (SOAT)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:12:49'
last_reinforced: '2026-04-30T02:12:49'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

## Overview

**Scene- and Object-Aware Transformer (SOAT)** is a [[transformer]] ⚠️ ⚠️-based Vision-and-Language Navigation agent designed for instruction-following in 3D environments. Unlike prior models that rely solely on global scene features or object-level features, SOAT **uses** two complementary visual encoders—a scene classification network ⚠️ and an object detector ⚠️—to better align visual observations with natural language instructions. The model also **leverages** vision-and-language pretraining on large-scale web data to bootstrap its understanding of visual-linguistic correspondences.

## Architecture

SOAT adopts a [[transformer]] ⚠️ ⚠️ architecture with two parallel visual pathways:

- **Scene encoder**: a scene classification network that outputs high-level contextual features (e.g., room type, layout cues).  
- **Object encoder**: an object detector that extracts region-level features for discrete objects in the view.  

These two streams are fused and passed through a cross-modal transformer that attends to the language instruction. The integration of scene-level context helps resolve ambiguities during object-level processing.

## Capabilities

On standard benchmarks:

- **Room-to-Room (R2R)**: improves Success weighted by Path Length (SPL) by **1.8% absolute** over prior methods.  
- **Room-Across-Room (RxR)**: improves Success Rate (SR) by **3.7% absolute**.  
- Demonstrates **stronger performance** on instructions containing **six or more object references**, indicating that dual-level visual encoding is especially beneficial for complex, reference‑heavy directions.

## Relationships

- **Uses**  
  - Scene Classification Network ⚠️  
  - Object Detector ⚠️  
  - Vision-and-Language Pretraining  

- **Depends On**  
  - Room-to-Room (R2R) dataset  
  - Room-Across-Room (RxR) dataset  

## See Also

- Transformer ⚠️  
- Vision-and-Language Navigation  
- Sim-to-Real Transfer (for related embodied navigation work)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Scene- and Object-Aware Transformer (SOAT)` --based_on ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `Scene- and Object-Aware Transformer (SOAT)` --based_on ⚠️ ⚠️--> `Room-Across-Room (RxR)`
