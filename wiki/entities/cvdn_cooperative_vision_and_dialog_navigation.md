---
id: cvdn_cooperative_vision_and_dialog_navigation
title: CVDN (Cooperative Vision-and-Dialog Navigation)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:38:18'
last_reinforced: '2026-04-30T01:38:18'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

# CVDN (Cooperative Vision-and-Dialog Navigation)

## Overview

**CVDN** (Cooperative Vision-and-Dialog Navigation) is a benchmark dataset and task designed to evaluate an agent's ability to follow dialogue-based instructions in a visual environment. Unlike standard Vision-and-Language Navigation (VLN) tasks that rely on static, human‑generated navigation instructions, CVDN introduces an interactive dialog setting: an `oracle` (human) provides step‑by‑step guidance through natural language, and the agent must ground these instructions in real‑time visual observations. This benchmark tests not only visual grounding and path planning, but also the ability to maintain dialogue context and ask clarifying questions when instructions are ambiguous.

CVDN is a **part of** the broader VLN benchmarks ⚠️ ⚠️ suite, which includes other navigation tasks such as R2R, REVERIE, and Touchdown ⚠️.

## Task Parameters

| Parameter | Value |
|-----------|-------|
| **Task** | Vision-and-language navigation with dialogue instructions |
| **Dataset type** | Benchmark |

## Capabilities

- **Dialogue‑based instruction following** – The agent must interpret and execute navigation commands that are delivered via a cooperative dialogue, often requiring back‑and‑forth clarification.
- **Visual‑language grounding** – The agent maps language utterances to specific objects and spatial relations in a 3D environment.
- **Context maintenance** – The agent must keep track of the dialogue history and update its internal state as new instructions arrive.

## Relationships

- **part_of** → VLN benchmarks ⚠️ ⚠️ – CVDN is one of the standard evaluation tasks for vision‑and‑language navigation research.
- **depends_on** → Visual Simulation Environments ⚠️ (e.g., Matterport3D Simulator) – The benchmark runs within photorealistic 3D environments.
- **depends_on** → Dialogue Management ⚠️ – The interactive nature of the task requires the agent to parse and respond to turn‑based dialog.

## Source

- **Paper**: *CVDN: Cooperative Vision‑and‑Dialog Navigation* (arxiv:2308.12587)  
- **Type**: Research benchmark definition

## See Also

- Vision-and-Language Navigation – The broader research area.
- Embodied Question Answering ⚠️ – Another task combining dialog and visual navigation.
- Human‑in‑the‑Loop Evaluation ⚠️ – Methodology used for cooperative navigation benchmarks.
- Matterport3D ⚠️ – The underlying 3D dataset used in CVDN.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CVDN (Cooperative Vision-and-Dialog Navigation)` --related_to ⚠️--> `Vision-and-Language Navigation`
- `CVDN (Cooperative Vision-and-Dialog Navigation)` --depends_on ⚠️--> `Matterport3D Simulator`
