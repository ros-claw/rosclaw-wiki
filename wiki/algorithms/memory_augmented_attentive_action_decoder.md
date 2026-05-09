---
id: memory_augmented_attentive_action_decoder
title: Memory-augmented attentive action decoder
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:17:28'
last_reinforced: '2026-04-29T21:17:28'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

# Memory-augmented Attentive Action Decoder

## Description

The **Memory-augmented Attentive Action Decoder** is a neural network component that generates action sequences for navigation tasks. It operates by attending to both current visual-language representations (from perception) and a memory of past experiences, allowing the agent to leverage historical context when deciding the next action. This decoder is specifically designed to fuse vision and language representations while incorporating past memory experiences, making it well-suited for embodied tasks in the [[REVERIE]] benchmark.

## Components

The decoder consists of three main components:

- **Memory**: A store of past experiences (e.g., previously observed visual features, language embeddings, or action histories) that the decoder can query.
- **Attention**: An attention mechanism that weights the relevance of current perceptual inputs and memory items.
- **Action Generation**: A module that produces a distribution over navigation actions (e.g., move forward, turn left/right, stop) based on the attended representation.

## Capabilities

- Generate action sequences for navigation in complex environments
- Fuse vision and language representations into a single latent space
- Incorporate past memory experiences to improve decision consistency and long-horizon planning

## Relationships

- **Part of**: This decoder is a key component of the [[Two-stage Training Pipeline for REVERIE]], where it operates after a cross-modal feature extraction stage.
- **Depends on**: The decoder relies on [[pretrained cross-modal features]] ⚠️ to align visual observations with language instructions before memory-augmented decoding.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Memory-augmented attentive action decoder` --[[extends]] ⚠️--> `Two-stage Training Pipeline for REVERIE`
