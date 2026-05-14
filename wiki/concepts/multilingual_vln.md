---
id: multilingual_vln
title: Multilingual VLN
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:06:50'
last_reinforced: '2026-04-30T03:06:50'
supersedes: []
sources:
- papers/2010.07954.pdf
source_type: arxiv_paper
---

## Definition

Multilingual Vision-and-Language Navigation (Multilingual VLN) extends the standard Vision-and-Language Navigation (VLN) paradigm to multiple natural languages, enabling agents to follow navigation instructions expressed in diverse languages beyond English. This addresses systematic language biases present in existing VLN datasets and benchmarks, which predominantly focus on English-only instructions.

## Languages and Motivation

The primary implementation studied in Room-Across-Room (RxR) supports three languages:

- English ⚠️
- Hindi ⚠️
- Telugu ⚠️

The motivation for multilingual VLN is to build agents that can ground natural language instructions to visual environments **independently of the input language**, thus testing and improving the language-agnostic grounding capabilities of embodied agents.

## Capabilities

- Enables cross-lingual navigation research by providing parallel instruction sets in multiple languages.
- Tests language-agnostic grounding by requiring the agent to map semantically equivalent instructions from different languages to the same spatial path.
- Facilitates the development of more inclusive embodied AI systems that can operate in multilingual human environments.

## Related Concepts

- **Room-Across-Room (RxR)** – The dataset that introduces multilingual VLN with aligned English, Hindi, and Telugu instructions. Multilingual VLN is a core component of RxR.
- **Vision-and-Language Navigation (VLN) ⚠️ ⚠️** – The foundational task that multilingual VLN extends.
- **Language Grounding ⚠️ ⚠️** – The ability to map language to perception, which is tested across languages in this setting.

## Relationship Annotations

- `part_of` Room-Across-Room (RxR)  
- `extends` Vision-and-Language Navigation (VLN) ⚠️ ⚠️  
- `implements` Language Grounding ⚠️ ⚠️ (in a cross-lingual context)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multilingual VLN` --related_to ⚠️--> `Room-Across-Room (RxR)`
