---
id: object_grounding_sub_task
title: Object Grounding sub-task
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:17:15'
last_reinforced: '2026-04-29T21:17:15'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

# Object Grounding sub-task

## Overview

The **Object Grounding sub-task** is a cross-modal alignment pretraining phase within the Two-stage Training Pipeline for REVERIE. Its objective is to teach the agent *what to attend to* in a scene by aligning visual object features with corresponding language tokens. This enables the agent to **attend to relevant objects** in a visual environment when given a natural language instruction.

## Parameters

| Parameter | Value |
|-----------|-------|
| **Type** | Cross-modal alignment pretraining |
| **Objective** | Learn what to attend to |

## Capabilities

- Attend to relevant objects in the scene by grounding language references in visual observations.

## Description

This sub-task constitutes the first stage of the two-stage pipeline. During object grounding, the agent learns to map object-level visual features from the visual environment ⚠️ ⚠️ to words or phrases in the language instruction ⚠️ ⚠️. The alignment is typically achieved through contrastive or attention-based losses that force the model to focus on the correct target object. Success in this sub-task is a prerequisite for later Object Navigation ⚠️ ⚠️ and Embodied Instruction Following ⚠️ stages, where the agent must act upon the grounded objects.

## Relationships

- **Part of** → Two-stage Training Pipeline for REVERIE
- **Uses** → visual environment ⚠️ ⚠️, language instruction ⚠️ ⚠️

## See also

- Object Navigation ⚠️ ⚠️
- Cross-modal Feature Alignment ⚠️
- REVERIE (task)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Object Grounding sub-task` --extends ⚠️--> `Two-stage Training Pipeline for REVERIE`
