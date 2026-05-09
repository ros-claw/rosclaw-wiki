---
id: object_centric_vln_oc_vln_dataset
title: Object-Centric VLN (OC-VLN) Dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:55:59'
last_reinforced: '2026-04-29T20:55:59'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Object-Centric VLN (OC-VLN) Dataset

The **Object-Centric VLN (OC-VLN) Dataset** is a benchmark dataset designed to evaluate the grounding of object-centric natural language navigation instructions. It focuses on zero-shot instruction following in multifloor home environments, requiring agents to interpret references to specific objects (e.g., "the red chair in the living room") and navigate accordingly.

## Purpose

The dataset serves primarily as an evaluation tool for assessing how well agents can follow object-centric navigation instructions without prior training on similar tasks (zero-shot). It tests the ability to map language to spatial-semantic knowledge of objects and their locations.

## Capabilities

- Provides a standardized benchmark for zero-shot object-centric instruction following.
- Includes instructions that reference specific objects in complex, multifloor home layouts.
- Enables evaluation of generalization across different object categories and spatial configurations.

## Context

The OC-VLN Dataset was introduced alongside the [[Language-Inferred Factor Graph for Instruction Following (LIFGIF)]] system in the same paper (arXiv:2411.07848). LIFGIF uses this dataset to demonstrate its ability to infer object-centric grounding without explicit training on the task.

## Relationships

- **used_by**: [[Language-Inferred Factor Graph for Instruction Following (LIFGIF)]] – the dataset was specifically created to evaluate LIFGIF's zero-shot performance on object-centric navigation.

## Related Entities

- [[Visual Language Navigation (VLN)]] ⚠️ – the broader research area that this dataset contributes to.
- [[Object-Centric Perception]] ⚠️ – the underlying concept of grounding language to objects in the environment.
- [[Zero-Shot Navigation]] – the evaluation setting the dataset targets.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Object-Centric VLN (OC-VLN) Dataset` --[[related_to]] ⚠️--> `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` _(wikilink)_
