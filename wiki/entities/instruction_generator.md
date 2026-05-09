---
id: instruction_generator
title: Instruction Generator
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:46:43'
last_reinforced: '2026-04-30T00:46:43'
supersedes: []
sources:
- papers/2412.08467.pdf
source_type: arxiv_paper
---

## Instruction Generator

The **Instruction Generator** is a text generation model responsible for producing high-quality navigational instructions. It serves as a core component of the [[Self-Refining Data Flywheel (SRDF)]] framework, converting raw navigational data into natural language guidance that can be used to train or evaluate autonomous agents.

### Parameters

- **Type**: Text generation model
- **Performance (SPICE)**: 26.2 (validated within the [[SRDF]] ⚠️ pipeline)

### Capabilities

- Generates precise, human-readable navigational instructions suitable for tasks such as path description, turning directions, and landmark-based guidance.

### Relationships

- **Used by**: [[Self-Refining Data Flywheel (SRDF)]] —— the generator provides instructions that are leveraged by the flywheel's training loop.
- **Trained on**: Filtered data from the [[Navigator]] (a separate entity that proposes candidate trajectories or paths). The filtered set ensures higher-quality training examples.

### Related Concepts

- [[Navigational Instructions]] ⚠️
- [[SPICE Metric (Semantic Propositional Image Caption Evaluation)]] ⚠️
- [[Data Flywheel]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Instruction Generator` --[[uses]] ⚠️--> `Self-Refining Data Flywheel (SRDF)`
