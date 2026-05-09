---
id: recurrent_vln_bert
title: Recurrent VLN-BERT
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:10:42'
last_reinforced: '2026-04-30T02:10:42'
supersedes: []
sources:
- papers/2203.02764.pdf
source_type: arxiv_paper
---

## Recurrent VLN-BERT

**Type**: Algorithm  
**Tags**: `vln`, `recurrent`, `bert`, `navigation`, `continuous-environments`  
**Confidence**: 0.8 (peer-reviewed paper: arxiv 2203.02764)

### Description

Recurrent VLN‑BERT is an extension of the original [[VLN-BERT]] model designed for Vision-and-Language Navigation. Unlike its predecessor, which operates over discrete graph nodes, this variant is adapted to **continuous environments** by integrating a [[Waypoints Predictor]] ⚠️ ⚠️. The agent takes high-level actions (node-to-node jumps) as in standard VLN, but the waypoint prediction module bridges the discrete-to-continuous gap.

### Parameters

- Action type: **high-level actions** – the agent moves by jumping between predicted waypoints rather than executing low‑level motor controls.

### Capabilities

- Navigates in continuous environments by predicting intermediate waypoints from discrete candidates.
- Improves discrete-to-continuous navigation gap by **18.24% SPL** (Success weighted by Path Length) over prior discrete VLN methods.

### Relationships

- **Uses** (uses): [[Waypoints Predictor]] ⚠️ ⚠️ – a learned module that predicts continuous waypoints from a discrete set of candidate nodes.
- **Depends on** (depends_on): [[VLN-BERT]] architecture (the recurrent BERT backbone for encoding instructions and visual observations).
- **Contributes to** (part_of): [[Vision-and-Language Navigation (VLN)]] ⚠️ research, specifically the continuous‑environment sub‑area.

### Notes

The paper demonstrates that adding recurrence to the VLN‑BERT agent (via an LSTM‑based memory) further stabilises navigation in novel continuous scenes. The waypoint predictor is trained jointly with the agent using a hybrid discrete‑continuous loss.

### Source

- arXiv:2203.02764 “Recurrent VLN‑BERT for Continuous Environment Navigation”