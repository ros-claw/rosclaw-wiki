---
id: open_vocabulary_maps
title: Open-Vocabulary Maps
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:39:05'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2403.09412.pdf
source_type: arxiv_paper
---

# Open-Vocabulary Maps

Open-Vocabulary Maps are a class of semantic map representations that leverage Visual-Language Models (VLMs) to understand and label spatial regions with arbitrary, natural language concepts, without requiring a predefined set of object classes. These environment representations enable robots to query and reason about their surroundings in flexible, human-like terms. They are typically deployed in **small-scale indoor environments**, where their ability to generalize to unseen objects is most effective.

## Key Enabler: Visual-Language Models (VLMs)

The fundamental capability of open-vocabulary maps is made possible by Visual-Language Models (VLMs) — models that align visual and textual representations. By embedding map regions into a shared vision-language space, these maps can associate any textual description (e.g., "clean surface", "something to sit on") with the corresponding geometry or location, enabling **zero-shot recognition** of arbitrary object classes without predefined labels.

## Capabilities

- **Zero-shot learning for arbitrary object classes**: The map can be queried for classes never seen during training, using only their textual description.
- **Support for open-set classes without retraining**: New categories can be added at runtime by simply providing new text prompts, eliminating the need to retrain the map generation pipeline.
- **Generalization to unseen objects**: The use of VLMs allows the map to respond to concepts far beyond the training ontology.

## Limitations: Scaling to Larger Environments

Existing open-vocabulary maps are designed primarily for small-scale indoor areas and face significant difficulty when scaling to large outdoor environments. The underlying understanding level (how deeply the VLM interprets spatial semantics) and the map structure (usually 2D or 2.5D grids) constrain performance in complex, unstructured outdoor scenes with many objects and intricate tasks. Addressing these **scalability challenges** is an active area of research.

## Relationship to Other Concepts

- **Supersedes**: Open-vocabulary maps supersede closed-vocabulary semantic maps ⚠️. Whereas closed‑vocabulary maps require a fixed ontology and often fail on unseen objects, open‑vocabulary maps generalize to any concept expressible in natural language.
- **Addressed by**: OpenGraph is a framework that directly targets the outdoor scaling limitation of open-vocabulary maps. OpenGraph builds open‑vocabulary graph‑based maps for long‑term robotic navigation, enabling persistent, queryable representations that can handle larger, more complex environments.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Open-Vocabulary Maps` --related_to ⚠️ ⚠️--> `Visual-Language Models (VLMs)` _(wikilink)_
- `Open-Vocabulary Maps` --related_to ⚠️ ⚠️--> `OpenGraph` _(wikilink)_