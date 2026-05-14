---
id: volume_state_estimation
title: Volume State Estimation
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:27:57'
last_reinforced: '2026-04-30T01:27:57'
supersedes: []
sources:
- papers/2403.14158.pdf
source_type: arxiv_paper
---

# Volume State Estimation

**Volume State Estimation** is a crucial algorithm in Vision-Language Navigation systems that uses current volumetric representations to maintain an Episodic Memory ⚠️ ⚠️ and predict the next navigation step. It encodes the agent’s state into a latent representation based on online collected Volumetric Environment Representation (VER) data.

## Description

Volume State Estimation leverages the current Volumetric Environment Representation to keep an episodic memory of the agent’s trajectory and surroundings. This memory is then used to predict the next navigation step, enabling closed-loop decision-making without full map reconstruction.

## Capabilities

- Estimates the current state from online collected volumetric representations.
- Feeds the estimated state into episodic memory for next‑step prediction.

## Relationships

| Relationship | Entity |
|---|---|
| uses | Volumetric Environment Representation |
| depends_on | Episodic Memory ⚠️ ⚠️ |
| part_of | Vision-Language Navigation |