---
id: pragmatic_reasoning
title: Pragmatic Reasoning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:46:38'
last_reinforced: '2026-04-30T02:46:38'
supersedes: []
sources:
- papers/1806.02724.pdf
source_type: arxiv_paper
---

## Pragmatic Reasoning

### Overview

Pragmatic Reasoning is a decision-making algorithm used within the Speaker-Follower Model that evaluates candidate action sequences by how well they explain a natural language instruction using the speaker model. This enables the follower to go beyond literal interpretation and select actions that a rational speaker would have described with that instruction.

### Description

Pragmatic reasoning in the Speaker-Follower Model uses the speaker model to score how well a sequence of actions explains a given natural language instruction. This allows the follower to consider whether its planned actions would be described by the instruction, leading to more accurate navigation.

### Parameters

| Parameter | Description |
|-----------|-------------|
| mechanism | Evaluates candidate action sequences by how well they explain an instruction using the speaker model |

### Capabilities

- Improves instruction follower decision-making
- Enables rational communication between speaker and listener

### Relationships

- **depends_on**: Speaker-Follower Model
- **part_of**: Speaker-Follower Model (peer component alongside the speaker model)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Pragmatic Reasoning` --extends ⚠️--> `Speaker-Follower Model`
