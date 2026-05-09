---
id: room_to_room_r2r
title: Room-to-Room (R2R)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:28:16'
last_reinforced: '2026-04-30T02:28:16'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

## Room-to-Room (R2R)

### Overview

Room-to-Room (R2R) is a standard benchmark for **vision-and-language navigation** (VLN) in indoor environments. It evaluates an agent's ability to follow natural language instructions to navigate through a series of connected rooms. The [[Scene- and Object-Aware Transformer (SOAT)]] achieves a **1.8% absolute improvement in SPL** on this benchmark.

### Benchmark Details

- **Type**: Navigation benchmark
- **Domain**: Indoor environments
- **Task**: Given a language instruction, the agent must traverse a path through a set of rooms (typically in a Matterport3D scene) to a target location.
- **Dataset**: Contains thousands of instruction‑path pairs collected in real-world indoor scans.

### Metrics

| Metric | Description |
|--------|-------------|
| SPL | **Success weighted by Path Length** – balances task success (reaching the target) with route efficiency. |
| SR  | **Success Rate** – binary success measure for whether the agent stops within a threshold distance of the goal. |

### Relationships

- **Used by**: [[Scene- and Object-Aware Transformer (SOAT)]] – SOAT leverages R2R as the primary evaluation benchmark.
- **Related to**: [[Room-Across-Room (RxR)]] – an extension of R2R that includes multilingual instructions and longer, more complex routes across multiple rooms and buildings.

> **Note on links**: [[SPL]] and [[Success Rate]] ⚠️ are common VLN metrics; if dedicated pages exist, they may be linked from here.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room-to-Room (R2R)` --[[related_to]] ⚠️--> `Room-Across-Room (RxR)`
