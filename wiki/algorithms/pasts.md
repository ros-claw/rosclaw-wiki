---
id: pasts
title: PASTS
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:12:49'
last_reinforced: '2026-04-29T21:12:49'
supersedes: []
sources:
- papers/2305.11918.pdf
source_type: arxiv_paper
---

# PASTS

**PASTS** (Pseudo-Action Spatio-Temporal Speaker) is a data augmentation algorithm for Vision-Language Navigation (VLN). It generates pseudo instructions from agent trajectories to improve the generalization of VLN models. PASTS achieves state-of-the-art performance on the R2R Dataset.

## Capabilities

- **Data augmentation**: Generates pseudo instructions by replaying agent trajectories, producing diverse training samples.
- **Improves generalization**: Helps VLN models generalize to unseen environments and novel language variations.
- **State-of-the-art performance**: Obtains top results on the R2R Dataset benchmark.

## Components

PASTS integrates three key modules:

- **Spatio-temporal encoder** – Encodes both spatial and temporal information from agent trajectories.
- **Speaker Progress Monitor (SPM)** – Monitors how far the agent has progressed along a trajectory to condition instruction generation.
- **Multifeature Dropout (MFD)** – Applies feature dropout on multiple input modalities to encourage robustness.

## Dependencies

- **depends_on**: Transformer ⚠️ – The underlying architecture for the spatio-temporal encoder and other components.

## Usage

PASTS can be combined with existing VLN models to boost their performance without modifying the model architecture. It is a plug-and-play augmentation technique **can_be_combined_with** VLN models ⚠️ such as HAMT, VLN-BERT, or any sequence‑to‑sequence VLN pipeline.

## References

- Original paper: *PASTS: Pseudo‑Action Spatio‑Temporal Speaker for Vision‑Language Navigation* (arxiv:2305.11918)
- See also: Vision-Language Navigation (VLN), R2R Dataset, Data Augmentation for VLN ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `PASTS` --extends ⚠️ ⚠️ ⚠️--> `Spatio-temporal encoder`
- `PASTS` --extends ⚠️ ⚠️ ⚠️--> `Speaker Progress Monitor (SPM)`
- `PASTS` --extends ⚠️ ⚠️ ⚠️--> `Multifeature Dropout (MFD)`
