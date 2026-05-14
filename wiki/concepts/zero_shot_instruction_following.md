---
id: zero_shot_instruction_following
title: Zero-shot Instruction Following
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:56:25'
last_reinforced: '2026-04-29T20:56:25'
supersedes: []
sources:
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Zero-shot Instruction Following

**Zero-shot Instruction Following** is a paradigm in Embodied AI where a system executes natural language navigation instructions in novel environments **without any additional training** (fine-tuning or adaptation) on the target environment or instruction set. The approach focuses on **object-centric** natural language navigation commands, enabling generalization to unseen spaces and task descriptions.

## Parameters

- **Approach**: No additional training on target environments or instructions.
- **Scope**: Object-centric natural language navigation instructions.

## Capabilities

- Generalize to novel environments without fine-tuning.
- Integrate Foundation Models with Traditional Navigation ⚠️ methods.

## Evaluation

The zero-shot instruction following paradigm was assessed on the OC-VLN ⚠️ dataset, comparing against Object Goal Navigation and Vision Language Navigation baselines. Results demonstrate competitive performance despite the lack of environment-specific training, highlighting the efficacy of combining large-scale pre-trained components with classical navigation stacks.

## Relationships

Zero-shot Instruction Following is *implemented by* the **Language-Inferred Factor Graph for Instruction Following (LIFGIF)** system, a representative architecture that decomposes instruction understanding and path planning into factor graph inference without task-specific fine-tuning.

Key dependencies:
- *depends_on*: Large Language Models for instruction parsing, Visual Foundation Models ⚠️ for object grounding
- *uses*: Factor Graphs ⚠️ for probabilistic reasoning over navigation subgoals
- *contrasts_with*: Fully Supervised Instruction Following ⚠️ which requires training on each target environment
- *part_of*: the broader field of Zero-shot Robot Navigation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-shot Instruction Following` --related_to ⚠️--> `Language-Inferred Factor Graph for Instruction Following (LIFGIF)` _(wikilink)_
