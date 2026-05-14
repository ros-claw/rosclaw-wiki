---
id: zero_shot_object_goal_visual_navigation
title: Zero-shot object goal visual navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:27:49'
last_reinforced: '2026-04-30T04:27:49'
supersedes: []
sources:
- papers/2206.07423.pdf
source_type: arxiv_paper
---

# Zero-shot Object Goal Visual Navigation

**Zero-shot object goal visual navigation** is a object goal visual navigation paradigm that extends the navigation capability to find target objects from **novel classes** that were not seen during training. Instead of relying on class-specific visual features or training samples for every possible target, this approach leverages **semantic similarities** between known and unknown classes to generalize the navigation policy.

## Description

Zero-shot object goal visual navigation addresses the limitation of traditional object goal navigation, which requires the robot to have been trained or fine-tuned on the exact set of target object categories. By using semantic embeddings—such as those derived from language models or knowledge graphs—the robot can infer the visual characteristics of an unseen target by comparing it to objects it has encountered before. This enables the robot to navigate to a target described only by its name or a brief description, without needing any additional training data for that specific class.

## Capabilities

- Guide a robot to locate and approach target objects from novel object classes without requiring any training samples of those classes.
- Generalize navigation policies across semantically related categories (e.g., from "chair" to "sofa").

## Relationships

- **is_a**: object goal visual navigation — it is a specialized form of navigation that incorporates zero-shot generalization.
- **uses**: Semantic Similarity Network (SSNet) — a neural architecture that computes semantic similarity between the target object description and observed scene features, enabling zero-shot inference.

## Related Concepts

- Embodied AI
- Visual Navigation
- Semantic Embeddings ⚠️
- Novel Object Detection ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-shot object goal visual navigation` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Zero-shot object goal visual navigation` --related_to ⚠️ ⚠️--> `Semantic Similarity Network (SSNet)` _(wikilink)_
