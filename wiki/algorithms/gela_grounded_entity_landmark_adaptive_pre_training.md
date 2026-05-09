---
id: gela_grounded_entity_landmark_adaptive_pre_training
title: GELA (Grounded Entity-Landmark Adaptive Pre-training)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:09:52'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

# GELA (Grounded Entity-Landmark Adaptive Pre-training)

## Overview

**GELA (Grounded Entity-Landmark Adaptive Pre-training)** is a pre-training paradigm within the [[VLN pre-training paradigm]] ⚠️ ⚠️ for [[Vision-and-Language Navigation (VLN)]] ⚠️. It explicitly supervises fine-grained alignment at the entity level using grounded entity-landmark annotations. GELA addresses the limitation of previous VLN pre-training methods that focus on image-level or region-level alignment, lacking explicit grounding of textual entities (e.g., "the red chair") to specific landmarks in the environment.

## Parameters

GELA adopts an **adaptive, grounded** pre-training paradigm distinguished by three complementary objectives. These objectives force the model to learn fine-grained correspondences between language entities and visual landmarks.

### Pre-training Objectives

1. **Entity phrase prediction** – The model learns to predict entity phrases from the navigational instruction and ground them in visual regions (e.g., mapping “the blue sofa” to specific pixels).
2. **Landmark bounding box prediction** – The model predicts the spatial locations of landmarks referenced in the instruction, creating explicit spatial associations between words and geometry.
3. **Entity-landmark semantic alignment** – A contrastive alignment loss maximizes agreement between entity phrase embeddings and corresponding landmark visual features, enforcing cross-modal consistency between text and vision.

These three objectives work together to produce a representation that is both linguistically precise and spatially aware.

## Capabilities

- Achieves **fine-grained cross-modal alignment** at the entity level, significantly improving instruction understanding and visual grounding.
- **State-of-the-art performance** on the [[Room-to-Room (R2R)]] benchmark and the [[CVDN (Cooperative Vision-and-Dialog Navigation)]] benchmark, demonstrating strong generalization to both descriptive (single-step) and dialogue-based navigation tasks.
- The learned representations are **generalizable across descriptive and dialogue instruction VLN tasks**, making GELA a versatile backbone for diverse navigation settings.

## Relationships

- **uses**: [[GEL-R2R dataset]], [[Room-to-Room (R2R) dataset]], [[CVDN dataset]] ⚠️
- **depends_on**: [[vision-and-language navigation]], [[cross-modal alignment]]
- **part_of**: [[VLN pre-training paradigm]] ⚠️ ⚠️
- **evaluated_on**: [[R2R]], [[CVDN]]

## References

- Source: `data/raw/papers/2308.12587.pdf`
- Reinforced by: subsequent analysis confirming objectives and paradigm classification.