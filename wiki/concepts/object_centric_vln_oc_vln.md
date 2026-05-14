---
id: object_centric_vln_oc_vln
title: Object-Centric VLN (OC-VLN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:42:33'
last_reinforced: '2026-04-30T00:42:33'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

## Object-Centric VLN (OC-VLN)

**Object-Centric VLN (OC-VLN)** is a dataset ⚠️ designed to evaluate the grounding of object-centric natural language navigation instructions. It provides a benchmark ⚠️ for zero-shot instruction following and is used to compare the Language-Inferred Factor Graph for Instruction Following (LIFGIF) against other baseline methods.

### Overview

OC-VLN focuses on the task of object-centric visual language navigation ⚠️, where an agent must follow natural language commands that refer to specific objects in a scene. Unlike standard VLN benchmarks, OC-VLN requires explicit object-level understanding and reasoning to successfully navigate.

### Purpose

- **Evaluate grounding** of object-centric navigation instructions.
- **Benchmark** for zero-shot instruction following without task-specific fine-tuning.

### Usage in Research

The dataset is primarily used to assess the performance of the Language-Inferred Factor Graph for Instruction Following (LIFGIF) approach. LIFGIF leverages object-centric factor graphs to interpret and follow instructions in OC-VLN, and the dataset serves as a common evaluation platform to compare against baselines.

### Relationships

- **Used by:** Language-Inferred Factor Graph for Instruction Following (LIFGIF)
- **Depends on:** Visual Language Navigation ⚠️ (VLN) task definition
- **Related to:** Object-Centric Reasoning ⚠️, Zero-Shot Learning

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Object-Centric VLN (OC-VLN)` --related_to ⚠️--> `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` _(wikilink)_
