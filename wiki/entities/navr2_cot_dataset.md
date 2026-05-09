---
id: navr2_cot_dataset
title: NavR^2-CoT dataset
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:05:13'
last_reinforced: '2026-04-30T00:05:13'
supersedes: []
sources:
- papers/2512.02400.pdf
source_type: arxiv_paper
---

# NavR^2-CoT Dataset

The **NavR^2-CoT Dataset** is a specialized dataset designed to train embodied navigation models in chain-of-thought (CoT) reasoning for open-vocabulary object-goal navigation. It provides structured supervision that helps models learn to perceive their environment, identify target-related objects in the surrounding context, and generate coherent action plans through step-by-step reasoning.

## Description

This dataset was constructed to teach a model three core abilities in sequence:

1. **Environmental perception** – recognizing and describing the current scene.
2. **Contextual focus** – identifying objects relevant to the goal object in the immediate surroundings.
3. **Action planning** – generating a future plan via structured CoT reasoning.

By decomposing the navigation task into these interpretable stages, the NavR^2-CoT Dataset aims to bridge the gap between low-level sensor data and high-level semantic decision-making in open-vocabulary settings.

## Relationship

The dataset is used by the [[Nav-R^2]] architecture to provide training examples that enforce structured reasoning. In turn, [[Nav-R^2]] implements the reasoning pipeline that consumes this dataset during training.

- **used_by**: [[Nav-R^2]]

## Source

Derived from the paper introducing Nav-R^2: *Nav-R^2: Chain-of-Thought Reasoning Meets Navigation* (arXiv:2512.02400).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `NavR^2-CoT dataset` --[[uses]] ⚠️--> `Nav-R^2`
