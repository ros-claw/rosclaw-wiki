---
id: open_vocabulary_mapping
title: Open-Vocabulary Mapping
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:01:09'
last_reinforced: '2026-04-30T00:01:09'
supersedes: []
sources:
- papers/2409.11764.pdf
source_type: arxiv_paper
---

# Open-Vocabulary Mapping

**Open-Vocabulary Mapping** is an environment representation ⚠️ technique that allows a robot to query arbitrary object classes using natural language, without requiring a fixed, pre-defined label set. It is a core component of semantic mapping ⚠️ ⚠️ and embodied AI, enabling systems to understand and interact with scenes in a flexible, human-interpretable way.

## Overview

Traditional semantic maps rely on a fixed taxonomy of object categories (e.g., only “chair”, “table”, “door”). Open-Vocabulary Mapping replaces this with continuous embeddings produced by open-vocabulary vision models, allowing the robot to answer queries like “find the red mug” or “where is the dog?” without prior training on those specific labels. This capability is essential for zero-shot object search and generalisation to novel environments.

## Capabilities

- **Arbitrary natural language queries**: Users can describe any object class in free-form text, and the map returns candidate locations.
- **Zero-shot object search**: The robot can find objects never seen during training, as long as an open-vocabulary vision model (e.g., CLIP, OWL-ViT) can relate the text description to visual features.
- **Integration with downstream tasks**: Open-vocabulary maps feed directly into navigation and manipulation policies, enabling truly flexible autonomous behaviour.

## Relationships

- **Part of**: semantic mapping ⚠️ ⚠️ · embodied AI
- **Used in**: OneMap · Zero-Shot Multi-Object Navigation

## Related Concepts

- Embedding-based scene representation ⚠️
- Natural language grounding ⚠️
- Open-Vocabulary Vision Models ⚠️ (e.g., CLIP, ALIGN)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Open-Vocabulary Mapping` --related_to ⚠️ ⚠️--> `embodied AI`
**Pending review:**
- `Open-Vocabulary Mapping` --related_to ⚠️ ⚠️--> `OneMap` _(wikilink)_
