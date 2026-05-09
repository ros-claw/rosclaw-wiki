---
id: zero_shot_object_centric_instruction_following
title: Zero-shot Object-centric Instruction Following
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:43:12'
last_reinforced: '2026-04-30T00:43:12'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Zero-shot Object-centric Instruction Following

## Overview

Zero-shot Object-centric Instruction Following is a [[Concept]] ⚠️ that enables a robot or agent to execute natural language instructions involving specific objects in previously unseen environments without any fine-tuning or environment-specific training. The paradigm combines the semantic understanding of [[Foundation Models]] (e.g., large language models, vision-language models) with the robust spatial mapping of traditional [[SLAM]] (Simultaneous Localization and Mapping) techniques. This integration allows the agent to ground abstract, object-referring commands to physical landmarks and execute them zero-shot.

## Parameters

| Parameter | Value |
|-----------|-------|
| **Paradigm** | Zero-shot |
| **Task** | Object-centric instruction following |
| **Integration** | Foundation models ↔ Traditional navigation ([[SLAM]], [[Mapping]] ⚠️) |

## Capabilities

- **No fine-tuning required for new environments** – The system generalizes directly from pre-trained components without additional data collection or model updates.
- **Ground natural language instructions to physical landmarks** – Translates expressions like "pick up the red cup on the table" into a sequence of navigational and manipulative actions anchored to real-world geometry and semantics.

## Relationships

- **Implemented by** → [[Language-Inferred Factor Graph for Instruction Following (LIFGIF)]] – This architecture realizes the zero-shot object-centric instruction following paradigm by constructing a factor graph from language cues and SLAM-based maps.

## Context

Zero-shot Object-centric Instruction Following bridges two historically separate research tracks: semantic grounding (often done in static datasets) and autonomous navigation (often done with geometric maps). By combining semantic understanding from foundation models with robust mapping from traditional SLAM techniques, it enables reactive, human-level command following in dynamic, real-world settings. The approach is particularly valuable for service robotics, warehouse automation, and assistive applications where rapidly deploying to new environments is critical.

---

*See also: [[Natural Language Grounding]] ⚠️, [[Factor Graphs]] ⚠️, [[Zero-shot Learning]], [[Object Detection]], [[Semantic Mapping]] ⚠️*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-shot Object-centric Instruction Following` --[[related_to]] ⚠️ ⚠️--> `SLAM` _(wikilink)_
- `Zero-shot Object-centric Instruction Following` --[[related_to]] ⚠️ ⚠️--> `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` _(wikilink)_
