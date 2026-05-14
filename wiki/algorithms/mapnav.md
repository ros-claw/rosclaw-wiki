---
id: mapnav
title: MapNav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:57:26'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2502.13451.pdf
source_type: arxiv_paper
---

# MapNav

**Type:** algorithm (specifically an end-to-end VLN model — see notes below)  
**Source:** arxiv paper `papers/2502.13451.pdf`

## Overview

**MapNav** is a novel end-to-end Vision-and-Language Navigation (VLN) model that replaces historical frame sequences with an Annotated Semantic Map (ASM). To reduce storage and computational overhead, it constructs a top-down semantic map of the environment at the start of each episode and updates it every timestep. The map is enhanced with explicit textual labels for key regions, derived from the underlying Vision-Language Model (VLM), allowing the agent to reason about both spatial layout and object semantics while following natural language instructions.

> **Note on classification:** The original source describes MapNav as an “end-to-end VLN model.” It is also categorized as a VLN **algorithm** in the general sense. Both descriptions are compatible; the more specific term is “end-to-end VLN model.”

## Parameters

| Parameter | Description |
|-----------|-------------|
| Model type | End-to-end VLN model (algorithm) |
| Input | Annotated Semantic Map (ASM) |
| Backbone | Vision-Language Model (VLM) |
| Output | Navigation actions (e.g., move forward, turn, stop) |
| Architecture | Uses a VLM as the core reasoning engine |

## Capabilities

- Navigates diverse unseen environments while following natural language instructions.
- Achieves state-of-the-art (SOTA) performance across both simulated and real-world settings.
- Reduces storage and computational overhead by eliminating long video history processing.

## Relationships

- **Uses:** Annotated Semantic Map (ASM), Vision-Language Model (VLM)
- **Depends on:** Vision-and-Language Navigation (task paradigm), semantic map construction, top-down mapping

## Performance

MapNav sets a new SOTA in both simulated benchmarks and real-world robot deployments. By replacing historical frames with the ASM, it enables efficient, real-time navigation that generalizes to novel environments without retraining.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MapNav` --based_on ⚠️ ⚠️--> `Annotated Semantic Map`
- `MapNav` --based_on ⚠️ ⚠️--> `Vision-and-Language Navigation`