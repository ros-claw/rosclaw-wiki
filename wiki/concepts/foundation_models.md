---
id: foundation_models
title: Foundation Models
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:55:21'
last_reinforced: '2026-04-30T00:55:21'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# Foundation Models

**Foundation Models** are large-scale pre-trained models (e.g., LLMs, VLMs) that exhibit broad, generalizable capabilities in perception, reasoning, and language understanding. They serve as a base for downstream tasks without requiring task-specific training, enabling zero-shot or few-shot adaptation.

## Role in Affordances-Oriented Planning

In the context of our knowledge base, Foundation Models are integrated into the AO-Planner architecture to achieve **affordances-oriented planning in a zero-shot setting**. Specifically, they are used to:

- Provide generalizable perception and reasoning across diverse environments and tasks.
- Interpret high-level task goals and infer actionable affordances without prior environment-specific data.

## Capabilities

- **Generalizable perception**: Foundation Models can recognize objects, spatial relationships, and scene contexts directly from visual or multimodal inputs.
- **Reasoning**: They support logical inference and decision-making, enabling the planner to chain actions toward a goal without explicit programming of preconditions.

## Relationships

- **Used by**: AO-Planner – The AO-Planner relies on Foundation Models as its core reasoning and perception module to perform zero-shot affordance planning.

## Source

- [AO-Planner paper (arxiv:2407.05890)](data/raw/papers/2407.05890.pdf) – Describes how Foundation Models are leveraged for affordances-oriented planning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Foundation Models` --related_to ⚠️--> `AO-Planner` _(wikilink)_
