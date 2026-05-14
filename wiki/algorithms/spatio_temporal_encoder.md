---
id: spatio_temporal_encoder
title: Spatio-temporal encoder
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:13:59'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2305.11918.pdf
source_type: arxiv_paper
---

## Spatio-temporal Encoder

The **Spatio-temporal encoder** is a core algorithmic component of the PASTS (Progress-Aware Spatio-Temporal Transformer Speaker) framework. It fuses panoramic representations and encodes intermediate connections across successive steps, enabling the system to capture both spatial structure and temporal dynamics in a unified representation.

### Overview

The spatio-temporal encoder processes input sequences by integrating panoramic observations (e.g., from a 360-degree camera or multiple sensors) and modeling how these representations evolve over time. By encoding intermediate connections through steps, it preserves dependencies across the sequence, making it suitable for tasks such as navigation, activity recognition, or embodied reasoning where both space and time are critical.

### Capabilities

- **Fuses panoramic visual representations** – Combines visual information from multiple viewpoints into a compact embedding.
- **Encodes intermediate connections across navigation steps** – Maintains temporal relationships between consecutive time steps, allowing the model to reason about short-term dynamics.

### Relationships

- **part_of** PASTS (Progress-Aware Spatio-Temporal Transformer Speaker) – The spatio-temporal encoder is a building block of the overall PASTS architecture, which stands for *Progress-Aware Spatio-Temporal Transformer Speaker*.

### Usage

The encoder is typically paired with a Spatio-temporal decoder ⚠️ or other downstream modules in PASTS to produce sequence outputs (e.g., action sequences, predictions). It may depend on Panoramic Representations ⚠️ and temporal attention mechanisms.

### References

- Introduced in the paper "PASTS: Progress-Aware Spatio-Temporal Transformer Speaker for Vision-and-Language Navigation" (arXiv:2305.11918).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Spatio-temporal encoder` --extends ⚠️--> `PASTS (Progress-Aware Spatio-Temporal Transformer Speaker)`