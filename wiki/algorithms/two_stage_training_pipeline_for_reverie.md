---
id: two_stage_training_pipeline_for_reverie
title: Two-stage Training Pipeline for REVERIE
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:16:10'
last_reinforced: '2026-04-29T21:16:10'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

## Overview

The **Two-stage Training Pipeline for REVERIE** is a learning architecture designed for the REVERIE task ⚠️ ⚠️ (Remote Embodied Referring Expressions). It enables an agent to localize a remote target object from a high-level natural language instruction and navigate to it in real indoor environments. The pipeline fuses vision and language representations with past memory experiences to generate accurate action sequences.

## Stages

The pipeline consists of two stages:

### Stage 1: Cross-modal Alignment Pretraining

In this stage, the agent is pretrained using two cross-modal alignment sub-tasks:

- **Scene Grounding ⚠️ ⚠️** – learns *where* to stop, i.e., which scene or region in the environment corresponds to the instruction.
- **Object Grounding ⚠️ ⚠️** – learns *what* to attend to, i.e., which specific object within the scene is referenced.

These sub-tasks align visual observations with linguistic cues without requiring explicit action supervision.

### Stage 2: Action Sequence Generation with Memory-augmented Decoder

In the second stage, a **Memory-augmented attentive action decoder** generates action sequences by fusing vision-language representations with past memory experiences. This allows the agent to maintain temporal context and improve navigation efficiency.

## Capabilities

- Localize remote target object from high-level instruction.
- Navigate in real indoor environments.
- Fuse vision and language representations with past memory.

## Relationships

- **Uses**:
  - Scene Grounding ⚠️ ⚠️ sub-task
  - Object Grounding ⚠️ ⚠️ sub-task
  - Memory-augmented attentive action decoder
- **Depends on**:
  - REVERIE task ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Two-stage Training Pipeline for REVERIE` --extends ⚠️--> `Memory-augmented attentive action decoder`
