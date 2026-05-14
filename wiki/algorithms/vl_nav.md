---
id: vl_nav
title: VL-Nav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:22:27'
last_reinforced: '2026-04-30T00:22:27'
supersedes: []
sources:
- papers/2502.00931.pdf
source_type: arxiv_paper
---

# VL-Nav

VL-Nav is a **neuro-symbolic navigation algorithm** designed to enable robots to navigate unseen large-scale environments by decomposing complex abstract instructions into executable subtasks. It combines neural reasoning with symbolic guidance to achieve robust, long-horizon navigation in both indoor and outdoor settings.

## Capabilities

- Navigate unseen large-scale environments based on complex abstract instructions.
- Decompose complex tasks into manageable subtasks.
- Perform efficient exploration guided by symbolic representations.

## Architecture

VL-Nav intertwines neural reasoning with symbolic guidance through two core components:

- **NeSy task planner**: Decomposes high‑level instructions into a sequence of symbolic subgoals using a VLM ⚠️ ⚠️ and a symbolic 3D scene graph.
- **NeSy exploration system**: Executes exploration actions, maintains an image memory system, and uses neuro‑symbolic inference to decide when to re‑localize or backtrack.

The system relies on a **symbolic 3D scene graph** to represent the environment spatially and an **image memory system** to store visual observations for later retrieval. A **VLM** (vision‑language model) provides grounding and commonsense reasoning.

## Key Dependencies

- `depends_on`: neuro-symbolic reasoning, symbolic 3D scene graph
- `uses`: NeSy task planner, NeSy exploration system, VLM ⚠️ ⚠️, image memory system

## Evaluation

VL-Nav was validated on the **DARPA TIAMAT Challenge** navigation tasks:

| Metric | Value |
|--------|-------|
| Indoor success rate | 83.4% |
| Outdoor success rate | 75.0% |
| Real‑world success rate | 86.3% |
| Maximum distance in real‑world run | 483 m |

## Source

This page is derived from the arxiv paper *VL‑Nav: A Neuro‑Symbolic Navigation Algorithm* (2502.00931).