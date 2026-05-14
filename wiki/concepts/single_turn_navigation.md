---
id: single_turn_navigation
title: Single-turn navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:15:52'
last_reinforced: '2026-04-30T03:15:52'
supersedes: []
sources:
- papers/2108.11544.pdf
source_type: arxiv_paper
---

# Single-turn navigation

**Single-turn navigation** is a category of Vision-Language Navigation (VLN) tasks in which navigation instructions are given once, at the beginning of the episode. The agent must interpret a single, complete instruction and execute the entire route without further clarification or revision from a human operator.

## Subtypes

Single-turn navigation is divided into two primary subtypes:

- **Goal-oriented navigation** — The instruction specifies only the final destination (e.g., “go to the kitchen”). The agent is free to choose the path as long as it reaches the target.
- **Route-oriented navigation** — The instruction describes a specific sequence of actions or landmarks (e.g., “turn left at the sofa, walk past the table, stop at the window”). The agent must follow the prescribed route.

Both subtypes fall under the broader umbrella of Vision-Language Navigation (VLN) and contrast with multi-turn navigation, where instructions are iteratively refined through dialogue.

## Relationship

- **part\_of**: Vision-Language Navigation (VLN)

---

**Source**: Paper 2108.11544 (arXiv)