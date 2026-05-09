---
id: formalized_cot_supervised_fine_tuning
title: Formalized CoT Supervised Fine-Tuning
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T01:03:40'
last_reinforced: '2026-04-30T01:03:40'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

## Overview

**Formalized CoT Supervised Fine-Tuning** is a skill within the [[EvolveNav]] pipeline. It applies structured [[Chain-of-Thought]] ⚠️ ⚠️ reasoning labels during supervised fine-tuning to activate navigational reasoning capabilities in a vision-language model and increase its reasoning speed. This skill constitutes the first training stage of EvolveNav, preparing the model for subsequent self-reflective post-training.

## Purpose

The primary purpose of Formalized CoT Supervised Fine-Tuning is to:
- Activate the model's navigational reasoning.
- Increase overall reasoning speed during navigation tasks.

It serves as the foundational stage (`stage: "first"`) in the [[EvolveNav]] training sequence.

## Capabilities

- **Activates navigational reasoning** – The fine-tuning process imbues the model with the ability to perform structured reasoning for navigation decisions.
- **Increases reasoning speed** – By learning from formalized CoT labels, the model produces faster inference compared to unguided or less structured approaches.

## Relationships

| Relationship | Target | Description |
|--------------|--------|-------------|
| `part_of` | [[EvolveNav]] | Formalized CoT SFT is the initial training stage of the EvolveNav framework. |
| `uses` | [[Chain-of-Thought|formalized CoT labels]] | The skill relies on curated, formalized CoT annotations as supervision. |
| `outputs_to` | [[Self-Reflective Post-Training]] | The fine-tuned model is passed to the next stage for self-reflective enhancement. |

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Formalized CoT Supervised Fine-Tuning` --[[uses]] ⚠️--> `EvolveNav`
