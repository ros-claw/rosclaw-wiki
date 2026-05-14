---
id: semi_automatic_cfg_construction_with_llms
title: Semi-automatic CFG construction with LLMs
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:28:44'
last_reinforced: '2026-04-30T01:28:44'
supersedes: []
sources:
- papers/2409.17313.pdf
source_type: arxiv_paper
---

## Overview

**Semi-automatic CFG construction with LLMs** is an algorithm that leverages Large Language Models to assist in building Context-Free Grammars ⚠️ ⚠️ (CFGs) for decomposing Vision-and-Language Navigation (VLN) tasks. By combining automated LLM-driven generation with human oversight, the method strikes a balance between efficiency and correctness, producing grammars that capture the hierarchical structure of navigation instructions.

## Method

The CFG is constructed semi-automatically with the help of LLMs. The process typically involves:

1. **Seed grammar design**: A human expert provides a small set of core rules or a template.
2. **LLM expansion**: The LLM proposes additional production rules, non-terminals, and terminal vocabularies based on example instructions and task schemas.
3. **Verification and pruning**: A human (or automated validator) checks the generated rules for consistency, coverage, and avoids ambiguities.
4. **Iterative refinement**: The LLM receives feedback and revises the grammar until it meets evaluation criteria.

This approach reduces manual effort while preserving the precision needed for VLN subtask decomposition.

## Capabilities

- **Constructs context-free grammars for VLN decomposition** – The output grammar is used to parse natural-language navigation commands into structured sub-goals, enabling Fine-grained evaluation framework for VLN.

## Relationships

- **used_in**: Fine-grained evaluation framework for VLN – The CFG is a core component for decomposing navigation instructions into measurable units, allowing fine-grained assessment of agent performance.
- **depends_on**: Large Language Models – The algorithm relies on LLMs for grammar rule generation and iterative improvement.
- **implements**: Context-Free Grammars ⚠️ ⚠️ – The method is a specific technique for constructing CFGs tailored to VLN tasks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Semi-automatic CFG construction with LLMs` --based_on ⚠️--> `Vision-and-Language Navigation`
