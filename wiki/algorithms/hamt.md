---
id: hamt
title: HAMT
type: algorithm
tags:
- vln
- transformer
- memory
- hierarchical
- r2r
confidence: 0.9
created_at: '2026-04-30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2101.07291.pdf
source_type: arxiv_paper
---

# HAMT (Hierarchical Adaptive Memory Transformer)

**HAMT** is a Vision-and-Language Navigation model that introduces a **hierarchical adaptive memory transformer** to efficiently encode long navigation histories. It addresses the scalability challenge in VLN where agents must remember and reason over hundreds of past observations across extended trajectories.

## Parameters

- **Type**: Hierarchical transformer navigation model
- **Task**: Vision-and-language navigation
- **Architecture**: Hierarchical transformer with adaptive memory compression
- **Memory levels**: 3 hierarchical levels (fine-grained, mid-level, coarse)
- **Visual encoder**: ResNet-152 or CLIP visual features
- **Text encoder**: BERT or RoBERTa language encoder
- **Trajectory encoding**: Hierarchical temporal attention over history
- **Action space**: Discrete (forward, turn left, turn right, stop)
- **Datasets**: [[R2R]], [[R4R]] ⚠️ ⚠️ ⚠️, [[RxR]], [[REVERIE]]

## Architecture

HAMT organizes navigation memory into three hierarchical levels:

1. **Frame-level memory**: Raw observation embeddings at each timestep
2. **Sub-trajectory memory**: Aggregated representations of short path segments
3. **Route-level memory**: Compressed representations of long-range trajectory structure

An **adaptive routing module** dynamically decides which memory level to access based on the current navigation context and instruction requirements. This enables efficient O(log n) attention over long histories instead of O(n).

## Key Innovations

- **Hierarchical memory compression**: Reduces computational complexity for long trajectories
- **Adaptive routing**: Dynamically selects appropriate memory granularity
- **Cross-modal hierarchical attention**: Aligns instruction tokens with multi-scale visual memories

## Capabilities

- Navigate long trajectories (R4R: 6+ room transitions) efficiently
- Scale to extended histories without linear attention cost
- Generalize across multiple VLN benchmarks with a single architecture

## Performance

On [[R2R]] test standard:
- **Success Rate (SR)**: ~63%
- **SPL (Success weighted by Path Length)**: ~57%

On [[R4R]] ⚠️ ⚠️ ⚠️ validation:
- **Success Rate**: ~47%
- **SPL**: ~42%

On [[RxR]] test:
- **Success Rate**: ~52%

## Relationships

- **Evaluates on**: [[R2R]], [[R4R]] ⚠️ ⚠️ ⚠️, [[RxR]], [[REVERIE]] — comprehensive benchmark coverage
- **Improves upon**: [[VLN-BERT]] — HAMT scales to longer trajectories via hierarchical memory
- **Related to**: [[Recurrent-VLN-BERT]] — both use BERT-based encoders but HAMT adds explicit hierarchy
- **Precedes**: [[DUET]] ⚠️ — later map-based methods build on HAMT's hierarchical reasoning

## See Also

- [[Vision-Language Navigation]] — the broader field
- [[Transformer]] ⚠️ — the underlying architecture
- [[Memory Networks]] ⚠️ — related memory-augmented neural architectures
- [[R2R]] — the primary benchmark

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HAMT` --[[implements]] ⚠️ ⚠️ ⚠️--> `R2R`
- `HAMT` --[[implements]] ⚠️ ⚠️ ⚠️--> `RxR`
- `HAMT` --[[implements]] ⚠️ ⚠️ ⚠️--> `REVERIE`
- `HAMT` --[[extends]] ⚠️ ⚠️--> `VLN-BERT`
- `HAMT` --[[extends]] ⚠️ ⚠️--> `Recurrent-VLN-BERT`
- `HAMT` --[[based_on]] ⚠️--> `Vision-Language Navigation`
