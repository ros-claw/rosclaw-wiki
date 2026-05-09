---
id: room2room_r2r_dataset
title: Room2Room (R2R) Dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:05:01'
last_reinforced: '2026-04-30T02:05:01'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

# Room2Room (R2R) Dataset

## Overview

The **Room2Room (R2R) Dataset** is a standard benchmark for **Vision and Language Navigation** ([[Vision and Language Navigation]]) in indoor environments. It is widely used to evaluate models that follow natural language instructions through real-world indoor spaces, such as [[VLN-Trans]]. The dataset is part of the broader [[Vision and Language Navigation Benchmarks]] ⚠️ ⚠️ suite, alongside related benchmarks like [[R4R]] ⚠️ ⚠️ ⚠️ and [[R2R-Last]] ⚠️ ⚠️ ⚠️.

## Description

The R2R dataset provides a set of navigation instructions paired with room-to-room trajectories. Each instruction describes a path from one room to another within a real indoor scene, and the agent must visually understand the environment and follow the instruction step by step. The dataset serves as the primary evaluation benchmark for the [[VLN-Trans]] approach, which learns cross-modal representations for this task. R2R is also used in conjunction with extensions such as [[R4R]] ⚠️ ⚠️ ⚠️ and [[R2R-Last]] ⚠️ ⚠️ ⚠️ for more targeted evaluations.

## Relationships

- **Used by**: [[VLN-Trans Evaluation]] ⚠️ — the dataset is the core testbed for performance comparison.
- **Part of**: [[Vision and Language Navigation Benchmarks]] ⚠️ ⚠️ — R2R is one of the foundational benchmarks in this family.

## See Also

- [[R4R]] ⚠️ ⚠️ ⚠️ — another benchmark dataset for room-to-room navigation with randomized instructions.
- [[R2R-Last]] ⚠️ ⚠️ ⚠️ — a variant focused on the final segment of navigation instructions.
- [[Vision and Language Navigation]] — the broader research area.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room2Room (R2R) Dataset` --[[related_to]] ⚠️ ⚠️--> `Vision and Language Navigation`
**Pending review:**
- `Room2Room (R2R) Dataset` --[[related_to]] ⚠️ ⚠️--> `VLN-Trans` _(wikilink)_
