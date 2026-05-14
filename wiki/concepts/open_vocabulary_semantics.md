---
id: open_vocabulary_semantics
title: Open-Vocabulary Semantics
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:14:07'
last_reinforced: '2026-04-30T01:14:07'
supersedes: []
sources:
- papers/2410.06239.pdf
source_type: arxiv_paper
---

# Open-Vocabulary Semantics

**Open-Vocabulary Semantics** refers to the capability of a robotic system to understand and label objects, locations, or scenes using a vocabulary that is not limited to a predefined set of training categories. It enables the robot to recognise and reason about arbitrary entities based on natural language descriptions, even if those specific entities were never seen during training.

## Overview

In embodied AI, open-vocabulary semantics bridges the gap between sensory perception and language. By fusing pre-trained vision-language models or large language models with sensor data (e.g., RGB-D cameras, LiDAR), a robot can construct rich, language-grounded representations of its environment. This approach is essential for tasks that require flexible human-robot interaction, such as following commands like "pick up the red mug next to the stack of notebooks."

## Capabilities

- **Zero-shot recognition**: Understand and locate objects or regions that were not present in the training dataset.
- **Generalisation to novel descriptions**: Respond to arbitrary natural language queries about the environment (e.g., "find the cleanest surface").
- **Integration with scene understanding**: The open-vocabulary output can be embedded into geometric or semantic maps, enabling tasks like object search, navigation, and manipulation.

## Usage

Open-vocabulary semantics is used in Hierarchical Scene Graph Construction. In that context, raw sensory data is paired with language embeddings to produce a structured representation of the environment at multiple levels of abstraction—objects, rooms, zones, and their relationships. The resulting semantic object maps serve as a foundation for planning and reasoning.

## Relationship Annotations

- **uses**: Open-Vocabulary Semantics uses Vision-Language Models ⚠️ or Large Language Models (LLMs) to map natural language to sensory data.
- **used_in**: The concept is a core component of Hierarchical Scene Graph Construction, where it provides the language-grounded labelling of nodes and edges.
- **depends_on**: Relies on pre-trained Multimodal Embeddings ⚠️ and sensor data pipelines (e.g., RGB-D Segmentation ⚠️).
- **part_of**: Belongs to the broader field of Embodied AI and Semantic Mapping ⚠️.

## Further Reading

- Related algorithms: CLIP, GLIP ⚠️, OpenScene ⚠️
- Related concepts: Sim-to-Real Transfer, Language Grounding ⚠️, Object-Centric Representation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Open-Vocabulary Semantics` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Open-Vocabulary Semantics` --related_to ⚠️ ⚠️--> `CLIP` _(wikilink)_
