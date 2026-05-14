---
id: user_demand_instructions
title: User Demand Instructions
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:14:32'
last_reinforced: '2026-04-30T01:14:32'
supersedes: []
sources:
- papers/2502.11142.pdf
source_type: arxiv_paper
---

# User Demand Instructions

## Definition

User demand instructions are navigation commands that reflect natural user preferences, such as "go to the kitchen" or "find the red chair", as opposed to step-by-step directions. They capture the diverse ways users communicate navigation goals, adapting to individual communication styles and contexts.

## Parameters

- **Type**: Navigation instructions matching user communication styles. These instructions are generated to align with how a real user would naturally express a goal, rather than using rigid, pre-defined formats.

## Capabilities

- Describe destinations or state specific needs briefly (e.g., "take me to the library").
- Simulate various user roles during training or testing, enabling models to handle a wide range of communicative behaviors.

## Relationships

- `generated_by`: NavRAG — User demand instructions are produced by the NavRAG framework to create more realistic and diverse training data.
- `used_in`: Vision-and-Language Navigation (VLN) ⚠️ — These instructions serve as input queries in VLN tasks, replacing artificial step-by-step directions with human-like commands.

## Additional Context

User demand instructions are essential for bridging the gap between synthetic navigation benchmarks and real-world applications. By modeling diverse user demand instructions, systems can learn to interpret ambiguous or concise commands, improving robustness in human-robot interaction.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `User Demand Instructions` --related_to ⚠️--> `NavRAG` _(wikilink)_
