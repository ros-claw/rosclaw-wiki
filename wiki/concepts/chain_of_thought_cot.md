---
id: chain_of_thought_cot
title: Chain-of-Thought (CoT)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:02:48'
last_reinforced: '2026-04-30T01:02:48'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

# Chain-of-Thought (CoT)

**Type**: concept

**Source**: arxiv_paper source: 2506.01551.pdf ⚠️

## Overview

Chain-of-Thought (CoT) is a reasoning chain that structures intermediate steps in a decision-making process. In embodied navigation, it formalizes the sequence of observations, subgoals, and actions that lead to a final navigational decision, improving both accuracy and interpretability.

## Parameters

- **Type**: reasoning chain
- **Role in EvolveNav**: CoT provides formalized labels used for supervised fine-tuning and is self‑enriched during post‑training to refine the model’s reasoning capacity.

## Capabilities

- Improves navigational decision accuracy by decomposing complex tasks into manageable steps.
- Enhances interpretability, allowing human operators and downstream systems to trace why a particular action or path was chosen.

## Relationships

- **Depends on**: LLM ⚠️ (Large Language Model) — CoT reasoning is generated and processed by an underlying LLM.
- **Used by**: EvolveNav — CoT is a core component of the EvolveNav framework for both initial training and self‑reflective improvement.
- **Part of**: 
  - Formalized CoT Supervised Fine-Tuning — CoT labels are used as targets for initial supervised fine‑tuning.
  - Self-Reflective Post-Training — CoT chains are self‑enriched and refined during post‑training to improve consistency and generalization.

## References

- ArXiv paper 2506.01551 — *EvolveNav: Self-Reflective Post-Training for Robotic Navigation via Formalized Chain-of-Thought Reasoning*.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Chain-of-Thought (CoT)` --related_to ⚠️--> `EvolveNav` _(wikilink)_
