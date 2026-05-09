---
id: synthetic_sub_instruction_dataset
title: Synthetic Sub-Instruction Dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:04:31'
last_reinforced: '2026-04-30T02:04:31'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

## Synthetic Sub-Instruction Dataset

### Overview

The **Synthetic Sub-Instruction Dataset** is a purpose-built collection of synthetic sub-instructions designed to train models that interpret and act upon navigation instructions involving recognizable and distinctive landmarks. It was introduced as part of the [[VLN-Trans]] training pipeline to improve the handling of landmark-based language cues in vision-and-language navigation (VLN) tasks.

### Description

Created by the authors of the paper associated with this dataset, the Synthetic Sub-Instruction Dataset contains artificially generated sub-instructions that teach agents to recognize and respond to salient landmarks during navigation. The dataset directly supports the translator module and the navigation agent in [[VLN-Trans]], bridging the gap between coarse route instructions and fine-grained landmark grounding.

### Relationships

- **Used by**:
  - [[VLN-Trans]] — employs this dataset to train its translator and navigation components.
  - [[Navigation Agent Training]] ⚠️ — serves as a resource for training agents to interpret landmark-based sub-instructions.

- **Part of**:
  - [[VLN-Trans Training Pipeline]] ⚠️ — is a key component of the overall training framework for VLN-Trans.

### Usage

The dataset is primarily used in supervised training settings where the goal is to improve the agent's ability to decompose high‑level instructions into actionable sub‑tasks that reference distinctive landmarks. By providing explicit synthetic examples, it strengthens the model's generalization to real‑world navigation scenarios.

For further context, see also [[Landmark Grounding]] ⚠️ and [[Synthetic Data Generation in VLN]] ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Synthetic Sub-Instruction Dataset` --[[related_to]] ⚠️--> `VLN-Trans` _(wikilink)_
