---
id: cvdn
title: CVDN
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:07:45'
last_reinforced: '2026-04-30T01:07:45'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

## Overview

**CVDN** (Cooperative Vision-and-Language Navigation) is a benchmark for **Vision-and-Language Navigation (VLN)** that evaluates a model's ability to follow natural language instructions while interacting with a dynamic environment. Unlike single-agent VLN tasks, CVDN introduces a **dialog-based** setting where a human follower and a human commander collaborate via natural language to reach a goal. This makes it a challenging testbed for grounding language in perception and action.

CVDN is used as an evaluation benchmark in the **[[EvolveNav]]** framework, which is a self-evolution method for VLN agents that improves without human annotations.

## Relationship with EvolveNav

- **[[EvolveNav]]** *evaluates* its performance on CVDN.
- CVDN *tests* the ability of [[VLN models]] ⚠️ to handle cooperative dialog tasks.
- EvolveNav's results on CVDN demonstrate its effectiveness in leveraging self-improvement without requiring additional labeled data.

## Usage in Evaluation

CVDN provides a realistic setting where agents must:
- Understand and ground multi-turn dialog instructions.
- Adapt to a human partner's utterances.
- Navigate through a photorealistic environment (Matterport3D).

In the [[EvolveNav]] paper (arXiv: 2506.01551), CVDN is one of the benchmarks used to validate the framework's capacity to improve over prior state-of-the-art models without manual annotation.

## Key Characteristics

- **Type**: VLN benchmark.
- **Modality**: Vision, language, dialog.
- **Environment**: Matterport3D scenes.
- **Task**: Cooperative navigation with human-in-the-loop.

## See Also

- [[VLN]] ⚠️ – Vision-and-Language Navigation.
- [[EvolveNav]] – Self-evolution framework for VLN.
- [[Matterport3D]] ⚠️ – Dataset used by CVDN.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CVDN` --[[uses]] ⚠️--> `EvolveNav`
