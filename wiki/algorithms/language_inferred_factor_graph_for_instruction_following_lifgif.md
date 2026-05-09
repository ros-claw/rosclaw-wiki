---
id: language_inferred_factor_graph_for_instruction_following_lifgif
title: Language-Inferred Factor Graph for Instruction Following (LIFGIF)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:55:44'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Language-Inferred Factor Graph for Instruction Following (LIFGIF)

**LIFGIF** grounds natural language instructions in a factor graph map without requiring pre-training on the target environment, enabling zero-shot operation. It uses a [[Factor Graph]] to jointly represent spatial landmarks and instruction semantics, performing inference to infer the correct path.

## Overview

LIFGIF grounds natural language instructions in a factor graph map without requiring pre-training on the target environment, enabling zero-shot operation. This allows a robot to follow natural language navigation instructions in novel environments while the map is being constructed.

## Parameters

- **Approach**: zero-shot (no fine‑tuning in unfamiliar environments)
- **Input**: natural language instructions
- **Representation**: 3D factor graph map of landmarks

## Method

- **Zero-shot**: Operates without fine‑tuning in unseen environments.
- **Approach**: Constructs a factor graph that jointly represents spatial landmarks and instruction semantics, performing inference to infer the correct path.
- **Dependencies**: Relies on map construction during navigation and the ability to parse natural language instructions into graph constraints.

## Capabilities

- Follows natural language navigation instructions while the map is being built.
- Supports zero-shot object-centric instruction following – understands references to objects (e.g., “go to the red chair”) without prior task‑specific data.
- Robust navigation in the physical world while the map is constructed, enabling operation in new environments without pre‑mapping.

## Relationships

- **Uses**: [[Factor Graph]]; [[3D Landmark Graph]] ⚠️ (structured representation of the environment); [[Boston Dynamics Spot]] (hardware platform for deployment).
- **Depends on**: factor graph mapping; natural language instructions; map construction during navigation.
- **Evaluated against**: [[Object Goal Navigation]]; [[Vision Language Navigation]].

## Evaluation Dataset

The **OC-VLN (Object-Centric VLN)** dataset was created specifically to assess grounding of object‑centric natural language navigation instructions.

## Performance

On OC-VLN, LIFGIF **outperforms state‑of‑the‑art zero‑shot baselines** from both Object Goal Navigation and Vision Language Navigation across all reported metrics.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` --[[based_on]] ⚠️--> `Factor Graph`
- `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` --[[implements]] ⚠️--> `Boston Dynamics Spot`