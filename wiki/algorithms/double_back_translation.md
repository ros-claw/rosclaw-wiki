---
id: double_back_translation
title: Double Back Translation
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:13:10'
last_reinforced: '2026-04-29T21:13:10'
supersedes: []
sources:
- papers/2103.00852.pdf
source_type: arxiv_paper
---

# Double Back Translation

## Overview

**Double Back Translation** is a training paradigm for Vision-and-Language Navigation (VLN) ⚠️ ⚠️ that enforces crossmodal consistency by learning two complementary mappings: path → instruction and instruction → path. This cycle-consistent approach forces the model to maintain a shared latent representation between linguistic and visual modalities, improving both navigation accuracy and instruction generation quality.

The technique is a core component of the CrossMap Transformer architecture, where it serves as a supervisory signal to align visual and textual embeddings without requiring parallel path–instruction pairs at inference time.

## Parameters

| Parameter | Description |
|-----------|-------------|
| Direction 1 | **path → instruction**: Generates a natural language instruction from a navigational path |
| Direction 2 | **instruction → path**: Reconstructs the navigational path from a generated or real instruction |

The two directions are learned jointly, and the consistency between the original path and the reconstructed path (or between original and generated instruction) acts as a self-supervision loss.

## Capabilities

- Translates generated navigation paths back into natural language instructions (Direction 1)
- Translates generated instructions back into navigation paths (Direction 2)
- Forces shared latent representations for crossmodal consistency, reducing modality gap in VLN ⚠️ benchmarks

## Relationships

- **uses** Transformer ⚠️ as the backbone sequence model for both translation directions
- **uses** CrossMap Transformer as the specific implementation that integrates double back translation with cross‑modal attention
- **depends_on** Vision-and-Language Navigation (VLN) ⚠️ ⚠️ as the task domain and evaluation framework
- **part_of** CrossMap Transformer – double back translation is a key training strategy within the CrossMap architecture

## Description

Double back translation is a training paradigm where two mappings are learned: path-to-instruction and instruction-to-path. This cycle-consistent approach reinforces the alignment between linguistic and visual modalities, improving both navigation and instruction generation. By reconstructing the input from its dual translation, the model learns to preserve task-relevant information across modalities, leading to more robust and interpretable embodied AI agents.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Double Back Translation` --extends ⚠️--> `CrossMap Transformer`
- `Double Back Translation` --based_on ⚠️--> `embodied AI`
