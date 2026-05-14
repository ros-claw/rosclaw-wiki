---
id: zero_shot_learning
title: Zero-Shot Learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:57:18'
last_reinforced: '2026-04-30T00:57:18'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# Zero-Shot Learning

**Zero-Shot Learning** refers to the ability of a model to generalize to tasks or categories it has never encountered during training, without requiring any task-specific fine-tuning or example data. In the context of Embodied AI and Vision-Language Navigation, zero-shot learning enables an agent to follow natural language instructions and navigate unseen environments purely through the compositional understanding of Foundation Models.

## Overview

Traditional machine learning models require labeled examples for each class or task. Zero-shot learning eliminates this need by leveraging semantic embeddings or multimodal representations (e.g., from Vision-Language Models ⚠️) to map novel inputs to known concepts. This is particularly valuable in dynamic, open-world settings where collecting task-specific training data is impractical.

## Application: Vision-Language Navigation

Zero-shot learning is applied within Vision-Language Navigation (VLN) systems to allow robots to interpret and execute new navigation instructions without prior exposure to the specific environment or linguistic variations. The agent uses Foundation Models pre-trained on large-scale vision-and-language corpora to reason about spatial relationships, object references, and action sequences in real time.

## Method

The central method involves deploying **foundation models** — such as CLIP, BLIP ⚠️, or GPT ⚠️ variants — that have been trained on massive, diverse datasets. These models encode visual scenes and text instructions into a shared embedding space, enabling zero-shot generalization. No task-specific training (e.g., fine-tuning on VLN datasets) is performed; the agent relies entirely on the model's pre-existing knowledge.

## Capabilities

- **Generalization without explicit training data:** The agent can handle novel instructions, object categories, and environmental layouts that were not part of any supervised VLN dataset.
- **Cross-modal reasoning:** Visual perception and linguistic understanding are unified, allowing natural language commands to directly influence navigation decisions.
- **Rapid adaptation:** Since no further training is needed, the system can be deployed to new tasks with zero cost in data collection or model retraining.

## Relationships

- **Used by AO-Planner:** The AO-Planner system incorporates zero-shot learning to enable adaptive, instruction-following navigation without prior environment-specific training. This allows AO-Planner to generalize across different robotic platforms and real-world spaces.

## See Also

- Foundation Models
- Sim-to-Real Transfer (related concept for generalization)
- Embodied Instruction Following ⚠️
- Zero-Shot Object Detection ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-Shot Learning` --related_to ⚠️ ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Zero-Shot Learning` --related_to ⚠️ ⚠️ ⚠️--> `CLIP` _(wikilink)_
- `Zero-Shot Learning` --related_to ⚠️ ⚠️ ⚠️--> `AO-Planner` _(wikilink)_
