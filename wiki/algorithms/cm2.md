---
id: cm2
title: CM2
type: algorithm
tags:
- vln
- cross-modal
- matching
- transformer
- reverie
confidence: 0.85
created_at: '2026-04-30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2011.03264.pdf
source_type: arxiv_paper
---

# CM2 (Cross-Modal Matching Model)

**CM2** is a cross-modal matching model for Vision-and-Language Navigation that addresses the challenge of grounding high-level natural language instructions in visual observations. It introduces a **cross-modal matching objective** that aligns textual and visual representations at multiple granularities, achieving strong performance on both fine-grained path-following ([[R2R]]) and high-level object-targeting ([[REVERIE]]) tasks.

## Parameters

- **Type**: Cross-modal transformer navigation model
- **Task**: Vision-and-language navigation
- **Architecture**: Bidirectional transformer with cross-modal attention
- **Visual encoder**: ResNet-152 or ViT features from panoramic views
- **Text encoder**: BERT-based language encoder
- **Matching levels**: Token-level, sentence-level, and trajectory-level
- **Training objectives**: Cross-modal matching + next-action prediction
- **Datasets**: [[R2R]], [[REVERIE]], [[RxR]]

## Method

CM2 introduces three complementary matching objectives:

1. **Token-level matching**: Align individual words with relevant image regions using cross-attention
2. **Sentence-level matching**: Score the compatibility between an instruction and a trajectory segment
3. **Trajectory-level matching**: Evaluate whether the full path satisfies the complete instruction

These objectives are jointly optimized during training, encouraging the model to learn robust cross-modal representations that generalize across different instruction granularities.

## Capabilities

- Handle both low-level (path-following) and high-level (object-finding) navigation instructions
- Improve cross-modal grounding through explicit matching supervision
- Transfer across VLN benchmarks without architecture changes

## Performance

On [[REVERIE]] validation:
- **Success Rate (SR)**: ~38%
- **Remote Grounding Success Rate (RGSR)**: ~32%

On [[R2R]] validation unseen:
- **Success Rate**: ~55%

## Relationships

- **Evaluates on**: [[REVERIE]] — demonstrates strong high-level instruction following
- **Also tests on**: [[R2R]] — shows generalization across task types
- **Related to**: [[VLN-BERT]] — both use BERT-based language encoders and cross-modal attention
- **Contrasts with**: [[HAMT]] — CM2 focuses on matching objectives while HAMT emphasizes hierarchical memory

## See Also

- [[Vision-Language Navigation]] — the broader field
- [[Cross-Modal Learning]] ⚠️ — the underlying learning paradigm
- [[REVERIE]] — the high-level instruction benchmark
- [[Transformer]] ⚠️ — the neural architecture

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CM2` --[[implements]] ⚠️ ⚠️ ⚠️--> `R2R`
- `CM2` --[[implements]] ⚠️ ⚠️ ⚠️--> `REVERIE`
- `CM2` --[[implements]] ⚠️ ⚠️ ⚠️--> `RxR`
- `CM2` --[[extends]] ⚠️ ⚠️--> `VLN-BERT`
- `CM2` --[[extends]] ⚠️ ⚠️--> `HAMT`
- `CM2` --[[based_on]] ⚠️--> `Vision-Language Navigation`
