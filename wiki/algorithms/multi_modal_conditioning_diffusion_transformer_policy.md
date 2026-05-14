---
id: multi_modal_conditioning_diffusion_transformer_policy
title: Multi-modal Conditioning Diffusion Transformer Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:52:02'
last_reinforced: '2026-04-29T20:52:02'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# Multi-modal Conditioning Diffusion Transformer Policy

The **Multi-modal Conditioning Diffusion Transformer Policy** is a lightweight algorithm that acts as **System 1** within the DualVLN framework. It is designed to "move fast" by executing low-level actions conditioned on high-level goals provided by the slower, more deliberative **System 2**. This policy leverages a Diffusion Transformer ⚠️ ⚠️ architecture and multi-modal conditioning ⚠️ ⚠️ to generate smooth, accurate trajectories in real time.

## Capabilities

- Generates smooth and accurate trajectories
- Leverages explicit pixel goals and latent features from System 2
- Enables real-time control and adaptive local decision-making

## Relationships

- **Part of**: DualVLN (the policy operates as the fast, reactive component within this two-system architecture)
- **Depends on**: Diffusion Transformer ⚠️ ⚠️ (as the core generative backbone) and multi-modal conditioning ⚠️ ⚠️ (to fuse pixel goals, latent features, and other modalities)

## Description

Acts as System 1 in DualVLN, a lightweight policy that "moves fast" by executing low-level actions conditioned on goals from System 2. It receives explicit pixel goals and latent features from the deliberative system and outputs continuous trajectory commands, enabling real-time local decision-making. The policy is trained to produce smooth, accurate motions while remaining computationally efficient enough for deployment on physical robots.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multi-modal Conditioning Diffusion Transformer Policy` --extends ⚠️--> `DualVLN`
