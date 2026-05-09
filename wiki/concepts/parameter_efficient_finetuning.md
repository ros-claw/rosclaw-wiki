---
id: parameter_efficient_finetuning
title: parameter_efficient_finetuning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:07:46'
last_reinforced: '2026-04-29T21:07:46'
supersedes: []
sources:
- papers/2403.07376.pdf
source_type: arxiv_paper
---

## Overview

**Parameter-Efficient Finetuning (PEFT)** is a set of techniques that adapt pre-trained large language models (LLMs) to downstream tasks by training only a small subset of parameters, dramatically reducing computational and memory costs while preserving the model's general knowledge. In the context of embodied AI and vision-and-language navigation, PEFT bridges the **domain gap** between a generic LLM training corpus and specialized task data (e.g., [[VLN]] ⚠️ ⚠️ ⚠️ trajectories) without requiring full model retraining.

## Capabilities

- Enables **self-guided navigational decision-making** with minimal additional parameters.
- **Mitigates the domain gap** between [[VLN]] ⚠️ ⚠️ ⚠️ task distributions and the original [[LLM]] ⚠️ ⚠️ training corpus.
- Provides a **cost-effective** alternative to full finetuning, making in-domain training feasible for resource-constrained scenarios.

## Relationships

- **Implements** cost-effective domain adaptation in [[NavCoT]].
- **Depends on** a pre-trained [[LLM]] ⚠️ ⚠️ backbone.
- **Used in** [[NavCoT]] to achieve in-domain training for navigational reasoning.

## Application in NavCoT

NavCoT fulfills parameter-efficient in-domain training, leading to significant mitigation of the domain gap in a cost-effective manner. By applying PEFT, the approach retains the language understanding capabilities of the base LLM while specializing it for the [[VLN]] ⚠️ ⚠️ ⚠️ task with only a fraction of the parameters being updated. This makes PEFT a cornerstone of NavCoT's design philosophy.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `parameter_efficient_finetuning` --[[related_to]] ⚠️--> `NavCoT` _(wikilink)_
