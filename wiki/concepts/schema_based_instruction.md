---
id: schema_based_instruction
title: Schema-based Instruction
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:06:12'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2312.02010.pdf
source_type: arxiv_paper
---

# Schema-based Instruction

**Type**: Concept  
**Confidence**: 0.8 (derived from peer-reviewed paper)  
**Source**: `papers/2312.02010.pdf`

## Overview

Schema-based instruction is a flexible framework that casts various navigation tasks into a unified text generation problem. This paradigm allows a single model to handle multiple task types (e.g., navigation, question answering, captioning) without requiring task-specific heads. By converting diverse task objectives into a common generative format, schema-based instruction enables a unified model across tasks, reduces architectural complexity, and simplifies the training pipeline.

## Key Attributes

| Parameter | Description |
|-----------|-------------|
| **Flexibility** | Casts various tasks into generation problems, supporting heterogeneous inputs and outputs. |
| **Unification** | Allows a single model to be trained on multiple tasks from different datasets. |

## Capabilities

- **Unifies task formats for training a single model** – Rather than training separate modules for each navigation objective, schema-based instruction provides a common interface that reduces architectural complexity.
- **Enables integration of diverse data sources from multiple datasets** – Because all tasks are expressed as text-in/text-out, data from different benchmarks (e.g., Room-to-Room, ScanNet, VLN-CE) can be mixed and used to train one shared encoder-decoder.
- **Allows training on multiple tasks with a single model** – By converting task specifications into a joint generation format, the same model can handle navigation, question answering, and captioning without task-specific heads.

## Usage in Models

Schema-based instruction is explicitly **used by** [[NaviLLM]], a large language model–based navigation agent that leverages this approach to perform visual navigation, question answering, and dense captioning with a single learned policy.

## Relationship Annotations

- **[[NaviLLM]]** `implements` *Schema-based instruction*
- *Schema-based instruction* `depends_on` `sequence-to-sequence generation` (implicit)
- *Schema-based instruction* `part_of` `task unification` in `embodied AI` (see [[Embodied AI]])

## Additional Context

By treating navigation commands, object grounding queries, and descriptive prompts as variations of a generative task, schema-based instruction reduces the need for handcrafted reward functions and auxiliary heads. This design aligns with the broader trend in [[Vision-Language-Action Models]] ⚠️ ⚠️ (VLA) that favor generative formulations over discriminative ones.

## Summary

Schema-based instruction allows LLMs to handle multiple embodied navigation tasks by converting task specifications into a joint generation format. This approach streamlines the training pipeline and promotes data reuse across diverse benchmarks.

## Related Pages

- [[NaviLLM]]
- [[Embodied AI]]
- [[Vision-Language-Action Models]] ⚠️ ⚠️
- [[Task Unification]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Schema-based Instruction` --[[related_to]] ⚠️--> `NaviLLM` _(wikilink)_