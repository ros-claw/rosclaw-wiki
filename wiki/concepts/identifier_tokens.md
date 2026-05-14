---
id: identifier_tokens
title: Identifier Tokens
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:39:37'
last_reinforced: '2026-04-30T00:39:37'
supersedes: []
sources:
- papers/2509.12129.pdf
source_type: arxiv_paper
---

# Identifier Tokens

**Identifier Tokens** are a key design element of the NavFoM architecture ⚠️ ⚠️ that encode contextual information about the embodiment and temporal state of a visual navigation task. They act as learnable embeddings that condition the model on the specific camera configuration and navigation horizon being used, enabling the same network to generalize across diverse robotic platforms and task settings.

## Function

Identifier tokens allow NavFoM to handle varying camera configurations and navigation horizons by providing explicit context to the model. Rather than retraining or switching network weights for each different setup, the model uses these tokens to adapt its internal representations on the fly, effectively "informing" the architecture which embodiment and time horizon are active.

## Capabilities

- **Embed camera view information of different embodiments** – The tokens capture the intrinsic and extrinsic parameters of the camera (field of view, resolution, mounting position) so that the model can correctly interpret visual input from robots with vastly different sensor layouts.
- **Encode temporal context of tasks** – In addition to spatial/embodiment cues, the tokens represent the current navigation horizon (i.e., short‑term vs. long‑term planning) and optionally the progress within a single task episode, enabling temporally aware decision making.

## Relationships

- `part_of` NavFoM architecture ⚠️ ⚠️ – Identifier tokens are a core component of the NavFoM framework, used alongside other modules (e.g., the token mixer, the action head).
- `enables` unified processing of diverse camera setups and horizons – Without these tokens, NavFoM would require separate models or manual feature normalization for each robotic platform; with them, a single set of weights can operate on data from multiple embodiments in a zero‑shot manner.

## Source

- Information extracted from the arxiv paper: `data/raw/papers/2509.12129.pdf` (Section on token design).