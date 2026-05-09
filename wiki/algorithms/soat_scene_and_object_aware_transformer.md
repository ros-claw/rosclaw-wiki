---
id: soat_scene_and_object_aware_transformer
title: SOAT (Scene- and Object-Aware Transformer)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:16:13'
last_reinforced: '2026-04-29T21:16:13'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

# SOAT (Scene- and Object-Aware Transformer)

**SOAT** is a transformer-based agent for [[Vision-and-Language Navigation]] (VLN) that explicitly models both high-level scene context and fine-grained object cues. It leverages two distinct visual encoders — a scene classification network for global context and an object detector for local object-level features — and benefits from [[Vision-and-Language Pretraining]] on large-scale web data.

## Overview

SOAT (Scene- and Object-Aware Transformer) improves a VLN agent’s ability to follow natural language instructions by fusing two complementary visual streams:

- **Scene features** capture the overall layout and semantic category of the current view (e.g., “kitchen”, “living room” from a [[Scene Classification Network]] ⚠️ ⚠️).
- **Object features** detect individual objects and provide fine-grained local cues (e.g., “chair”, “TV”) via an [[Object Detector]] ⚠️ ⚠️ ⚠️.

The scene features are used to support and contextualize the object-level processing, and the entire model is initialized from a vision-and-language pretrained transformer. This dual-encoder design allows the agent to better align instructions with visual observations, especially when the instruction contains multiple object references.

## Architecture & Parameters

| Parameter | Details |
|-----------|---------|
| **Visual encoders** | Scene classification network + object detector |
| **Core architecture** | Transformer-based |
| **Pretraining** | Vision-and-language pretraining from large-scale web data |

The transformer architecture processes a sequence of tokenized instruction words, past actions, and the current panoramic observation. Each observation branch (scene and object) produces a set of encoded features that are fused via cross-attention before action prediction.

## Capabilities

- End-to-end [[Vision-and-Language Navigation]] agent for environments like [[Room-to-Room (R2R)]] and [[Room-Across-Room (RxR)]].
- Achieves state-of-the-art performance at time of publication:
  - **+1.8% absolute SPL** on the R2R benchmark.
  - **+3.7% absolute SR** on the RxR benchmark.
- Significantly better alignment with instructions that contain six or more object references, demonstrating the advantage of explicit object detection.

## Evaluation Benchmarks

- [[Room-to-Room (R2R)]] – a standard VLN benchmark with photorealistic houses.
- [[Room-Across-Room (RxR)]] – a multilingual VLN dataset with longer, more descriptive instructions.

## Relationships

- **uses**:: [[Transformer]] ⚠️ architecture, [[Vision-and-Language Pretraining]], scene classification, object detection.
- **depends_on**:: [[Scene Classification Network]] ⚠️ ⚠️, [[Object Detector]] ⚠️ ⚠️ ⚠️, web-scale vision-and-language pretrained models.
- **evaluated_on**:: [[Room-to-Room (R2R)]], [[Room-Across-Room (RxR)]]

*See also:* [[Vision-and-Language Navigation]], [[Object Detector]] ⚠️ ⚠️ ⚠️, [[Transformer Models for VLN]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SOAT (Scene- and Object-Aware Transformer)` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
