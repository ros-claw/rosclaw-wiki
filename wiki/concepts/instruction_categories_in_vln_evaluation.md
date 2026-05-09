---
id: instruction_categories_in_vln_evaluation
title: Instruction categories in VLN evaluation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:29:12'
last_reinforced: '2026-04-30T01:29:12'
supersedes: []
sources:
- papers/2409.17313.pdf
source_type: arxiv_paper
---

# Instruction Categories in VLN Evaluation

**Instruction categories** are a set of five principal classes used to break down natural-language navigation instructions for fine-grained evaluation of [[Vision-Language Navigation]] (VLN) agents. These categories were derived from a context-free grammar (CFG) decomposition of typical VLN instructions, enabling researchers to analyze specific agent capabilities beyond overall success metrics.

## Categories

The taxonomy comprises five distinct categories:

- **Direction change** – Instructions that require the agent to alter its heading (e.g., “turn left”, “go straight”).
- **Landmark recognition** – Instructions referencing visual landmarks used for localization or orientation (e.g., “the red building”, “the fountain”).
- **Region recognition** – Instructions that involve identifying or entering a spatial region (e.g., “the kitchen”, “the hallway”).
- **Vertical movement** – Instructions about changing altitude or floor level (e.g., “go upstairs”, “take the elevator”).
- **Numerical comprehension** – Instructions containing quantitative information such as distances or counts (e.g., “walk 10 meters”, “the third door on the right”).

These categories are part of the [[Fine-grained evaluation framework for VLN]] and are applied to parse [[VLN instruction benchmarks]] ⚠️ for diagnostic analysis.

## Capabilities

- Categorizes instruction types for fine-grained evaluation.

## Relationships

- **Part of**: [[Fine-grained evaluation framework for VLN]]
- **Uses**: [[CFG decomposition]] ⚠️ to extract categories from natural language
- **Depends on**: [[Vision-Language Navigation]] task definition

## Usage

In practice, evaluating a VLN agent involves decomposing each instruction into its category components and measuring success rate per category. This reveals whether an agent struggles with, for example, landmark recognition or numerical comprehension, guiding targeted improvements in [[VLN model architecture]] ⚠️ or [[training data augmentation]] ⚠️.

## Sources

- Paper: *Fine-grained Evaluation of VLN Agents* (arXiv 2409.17313)