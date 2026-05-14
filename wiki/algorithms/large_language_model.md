---
id: large_language_model
title: Large Language Model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:19:10'
last_reinforced: '2026-04-30T04:19:10'
supersedes: []
sources:
- papers/2405.14093.pdf
source_type: arxiv_paper
---

# Large Language Model

A **Large Language Model (LLM)** is a type of algorithm ⚠️ trained on vast text corpora to perform language understanding ⚠️ and generation tasks. In the context of embodied AI, LLMs serve as high-level reasoning components that parse natural language instructions, generate action plans, and interface with perception and control stacks.

## Capabilities

- Language understanding and generation—enabling tasks such as instruction following, dialogue, and code synthesis.

## Role in Robot Learning

LLMs are foundational to Vision-Language-Action Model (VLA), where they provide language grounding and reasoning. In a typical VLA pipeline, an LLM ⚠️ processes user commands and context, then outputs latent representations or action tokens that are decoded into motor commands.

## Relationships

- **used_by**: Vision-Language-Action Model — VLA models depend on LLMs for language processing and planning.
- **part_of**: embodied AI stack — LLMs often sit alongside perception modules ⚠️ and control policies ⚠️.
- **implements**: natural language understanding ⚠️ — the core mechanism that enables human-robot interaction.

## Source

This page derives from the paper *Large-Scale Vision-Language-Action Models for Robot Manipulation* (arXiv:2405.14093).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Large Language Model` --based_on ⚠️--> `embodied AI`
