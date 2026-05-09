---
id: pasts_progress_aware_spatio_temporal_transformer_speaker
title: PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:53:32'
last_reinforced: '2026-04-30T01:53:32'
supersedes: []
sources:
- papers/2305.11918.pdf
source_type: arxiv_paper
---

## PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)

### Overview

PASTS is a speaker model for **[[Vision-and-Language Navigation]] (VLN)** that leverages a **[[Transformer]] ⚠️** core to attend to both spatial and temporal features of an agent's trajectory. It introduces a **Speaker Progress Monitor (SPM)** to align generated pseudo instructions with the agent's actual navigation progress, enabling high-quality data augmentation that boosts the generalization performance of downstream VLN agents.

### Architecture

PASTS consists of several key components:

- **Spatio-Temporal Encoder** – A Transformer-based encoder that processes the agent’s observed visual frames and action sequence, capturing spatial layouts and temporal dependencies.
- **Speaker Progress Monitor (SPM)** – A learned module that predicts how much of the instruction has been delivered relative to the trajectory progress. This ensures the synthetic instruction is temporally aligned with the navigation steps.
- **Multifeature Dropout (MFD)** – A dropout strategy applied to multiple feature modalities (e.g., visual, action) during training to improve robustness and prevent overfitting.

### Capabilities

- Generates pseudo instructions for data augmentation in VLN tasks.
- Enhances generalization performance of VLN agents, especially under limited training data.
- Outperforms existing **[[LSTM]]**-based speaker models on standard benchmarks.
- Achieves state-of-the-art performance on the **[[Room-to-Room (R2R)]]** dataset when used as a data augmentation module.
- Flexible: can be combined with any existing VLN model (e.g., [[VLN-BERT]], [[HAMT]]) to improve their navigation accuracy.

### Relationships

- **`uses`**: [[Transformer architecture]] ⚠️, [[Spatio-Temporal Encoder]], [[Speaker Progress Monitor]] ⚠️, [[Multifeature Dropout]] ⚠️
- **`depends_on`**: [[Vision-and-Language Navigation]] task, [[Trajectory Dataset]] ⚠️ (e.g., [[R2R]])
- **`improves_upon`**: [[LSTM-based speaker models]] ⚠️, [[Previous VLN models]] ⚠️ (when used for augmentation)
- **`part_of`**: [[Data augmentation pipeline for VLN]] ⚠️

### Performance Summary

On the R2R test set, PASTS-generated pseudo instructions improve the success rate and navigation efficiency of multiple downstream VLN agents (e.g., +X% SPL over baseline without augmentation). The SPM module is critical for instruction alignment, and MFD prevents mode collapse during training.

### References

- Original paper: *"Progress-Aware Spatio-Temporal Transformer Speaker for Vision-and-Language Navigation"* (arXiv:2305.11918)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
- `PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)` --[[extends]] ⚠️ ⚠️--> `LSTM`
- `PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)` --[[extends]] ⚠️ ⚠️--> `Spatio-Temporal Encoder`
