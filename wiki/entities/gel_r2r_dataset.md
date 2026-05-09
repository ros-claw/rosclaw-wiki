---
id: gel_r2r_dataset
title: GEL-R2R dataset
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:10:43'
last_reinforced: '2026-04-29T21:10:43'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

## GEL-R2R Dataset

### Overview

**GEL-R2R** (Grounded Entity-Landmark Room-to-Room) is an extension of the [[Room-to-Room (R2R)]] dataset that adds grounded entity-landmark human annotations. It was introduced alongside the [[GELA]] ⚠️ ⚠️ model for pre-training fine-grained cross-modal alignment in Vision-and-Language Navigation (VLN).

### Description

GEL-R2R enriches each instruction–path pair in the original R2R dataset with annotations linking specific entities (e.g., objects, furniture) and landmarks (e.g., doors, stairs) mentioned in the natural language instruction to their corresponding regions in panoramic images. These annotations enable models to learn precise spatial and semantic correspondences between language and visual observations, moving beyond coarse room-level or direction-based reasoning.

The dataset is designed to support pre-training of the Grounded Entity-Landmark Alignment (GELA) architecture, which explicitly aligns textual references with visual features in a contrastive learning framework.

### Parameters

| Parameter | Value |
|-----------|-------|
| Type | Dataset |
| Base dataset | [[Room-to-Room (R2R)]] |
| Annotations | Grounded entity–landmark human annotations |

### Capabilities

- Enables fine-grained cross-modal alignment training for VLN agents.
- Provides training data for models that need to locate specific objects and landmarks referenced in instructions.
- Supports improved generalization to unseen environments by teaching explicit grounding.

### Relationships

- **part_of** [[Room-to-Room (R2R)]] – GEL-R2R is a derivative dataset built on top of the original R2R data.
- **used_by** [[GELA]] ⚠️ ⚠️ – The dataset was created to pre-train the GELA model.
- **depends_on** [[Room-to-Room (R2R)]] – Inherits the path–instruction pairs and evaluation splits of R2R.

### Source

- arXiv paper: *Grounded Entity-Landmark Alignment for Vision-and-Language Navigation* (2308.12587)