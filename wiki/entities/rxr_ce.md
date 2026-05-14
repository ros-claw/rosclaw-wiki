---
id: rxr_ce
title: RxR-CE
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T20:48:49'
last_reinforced: '2026-04-29T20:48:49'
supersedes: []
sources:
- papers/2512.01550.pdf
source_type: arxiv_paper
---

## RxR-CE (Room-crossing Challenge with Continuous Environments)

**RxR-CE** (Room-Crossing Challenge with Continuous Environments) is a benchmark for evaluating embodied navigation agents in continuous, multi-room settings. It focuses on complex cross-room navigation instructions, testing an agent’s ability to follow natural language commands that require traversing through doorways and across different spaces.

### Domain

- **Embodied navigation** — part of the broader Room-Across-Room (RxR) dataset family.

### Relationships

- **Used by** → NavForesee as the evaluation platform for long-horizon, instruction-following navigation.

### Description

RxR-CE extends the original RxR benchmark by removing discrete abstractions—agents must operate in continuous environments (e.g., realistic 3D scans of buildings) rather than on a fixed graph of locations. The instructions are drawn from human‑annotated navigational descriptions involving multiple rooms, requiring the agent to understand spatial relationships, room transitions, and temporal ordering of sub‑goals. The benchmark is designed to stress‑test model generalization across unseen room layouts and instruction paraphrases.

### Key Characteristics

- **Continuous Action Space**: Agents move and rotate freely, avoiding grid‑based restrictions.
- **Multi‑Room Instructions**: Sample commands include “Exit the bedroom, turn right, walk through the living room, and stop at the kitchen table.”
- **Metric‑Driven**: Evaluated using success rate (SR) and navigation error (NE) under the RXREval framework.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `RxR-CE` --uses ⚠️--> `NavForesee`
