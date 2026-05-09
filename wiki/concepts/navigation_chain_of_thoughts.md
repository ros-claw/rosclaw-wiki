---
id: navigation_chain_of_thoughts
title: Navigation Chain of Thoughts
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:21:43'
last_reinforced: '2026-04-30T01:21:43'
supersedes: []
sources:
- papers/2405.10620.pdf
source_type: arxiv_paper
---

# Navigation Chain of Thoughts

**Navigation Chain of Thoughts** is a reasoning module within [[MC-GPT]] that leverages [[human_navigation_examples]] ⚠️ ⚠️ ⚠️ to produce diverse chains of reasoning for navigation tasks. It enriches navigation strategy diversity and improves decision-making in [[Visual Language Navigation (VLN)]] ⚠️.

## Key Insight

This approach addresses a fundamental limitation of prior LLM-based VLN systems: monolithic, single-path reasoning. By generating multiple, varied reasoning chains, the Navigation Chain of Thoughts module enables more robust and adaptive navigation behavior.

## Parameters

- **Based on**: [[human_navigation_examples]] ⚠️ ⚠️ ⚠️
- **Purpose**: Enrich navigation strategy diversity

## Capabilities

- Generates diverse navigation reasoning chains
- Improves decision-making in [[VLN]] ⚠️

## Relationships

- **part_of**: [[MC-GPT]]
- **uses**: [[Large Language Models]], [[human_navigation_examples]] ⚠️ ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Navigation Chain of Thoughts` --[[related_to]] ⚠️--> `MC-GPT` _(wikilink)_
