---
id: speaker_follower
title: Speaker-Follower
type: algorithm
tags:
- vln
- speaker-follower
- r2r
- seq2seq
confidence: 0.9
created_at: '2026-04-30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1806.02724.pdf
source_type: arxiv_paper
---

# Speaker-Follower

The **Speaker-Follower** model is a landmark approach to Vision-and-Language Navigation (VLN) that introduces a dual-model architecture: a **Speaker** that generates natural language instructions from trajectories, and a **Follower** that executes instructions to navigate. This framework enables data augmentation via synthetic instructions and significantly improved performance on the [[R2R]] benchmark.

## Parameters

- **Type**: Seq2seq navigation model with paired instruction generator
- **Task**: Vision-and-language navigation
- **Architecture**: LSTM-based encoder-decoder for both Speaker and Follower
- **Visual encoder**: ResNet-152 CNN features from panoramic views
- **Action space**: Discrete (forward, turn left, turn right, stop)
- **Training**: Imitation learning + reinforcement learning (speaker-driven data augmentation)
- **Datasets**: [[R2R]] (primary), [[R4R]] ⚠️ (extended)

## Architecture

### Follower
The Follower encodes the natural language instruction with an LSTM, then at each timestep attends over the instruction and current panoramic visual features to select the next action.

### Speaker
The Speaker encodes a trajectory (sequence of visual observations) and generates a natural language instruction that describes the path. It is trained on human instructions and used to:

1. **Augment training data** by generating synthetic instructions for unseen paths
2. **Score trajectory-instruction compatibility** during inference (pruning bad paths)
3. **Enable back-translation** for iterative data augmentation

## Capabilities

- Navigate indoor environments from natural language instructions
- Generate fluent, diverse synthetic navigation instructions
- Prune candidate paths using the speaker's probability score
- Achieve strong zero-shot transfer via data augmentation

## Performance

On [[R2R]] validation unseen:
- **Navigation Error (NE)**: ~4.6m (with data augmentation)
- **Success Rate (SR)**: ~53% (with data augmentation)
- **Oracle Success Rate (OSR)**: ~63%

## Relationships

- **Evaluates on**: [[R2R]] — the primary benchmark
- **Improved by**: [[EnvDrop]] — combining EnvDrop with Speaker-Follower yields better generalization
- **Extended by**: [[RCM]] ⚠️ — uses reinforcement learning to align speaker and follower more tightly
- **Precedes**: [[PREVALENT]] — later pretraining methods leverage the speaker-follower intuition at scale

## See Also

- [[Vision-Language Navigation]] — the broader research area
- [[R2R]] — the benchmark dataset
- [[Seq2Seq]] ⚠️ — the underlying sequence modeling paradigm
- [[Data Augmentation]] ⚠️ — the technique enabled by the Speaker module

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Speaker-Follower` --[[implements]] ⚠️ ⚠️--> `R2R`
- `Speaker-Follower` --[[extends]] ⚠️--> `EnvDrop`
- `Speaker-Follower` --[[implements]] ⚠️ ⚠️--> `PREVALENT`
- `Speaker-Follower` --[[based_on]] ⚠️--> `Vision-Language Navigation`
