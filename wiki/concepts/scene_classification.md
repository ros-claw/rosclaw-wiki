---
id: scene_classification
title: Scene Classification
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:23:28'
last_reinforced: '2026-04-30T02:23:28'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

## Scene Classification

**Scene Classification** is a computer vision task that assigns a semantic label (e.g., "bedroom", "kitchen", "outdoor") to an entire image or video frame. In the context of embodied AI and instruction following, scene classification provides high‑level contextual information that supports object‑level processing and grounding.

### Role in SOAT ⚠️ ⚠️

Within the Scene- and Object-Aware Transformer (SOAT) architecture, scene classification acts as one of two visual encoders. Its output features are aligned with scene‑level cues in natural language instructions (e.g., "go to the bedroom"). This allows the model to match scene descriptions from the instruction to the visual environment, improving spatial and referential understanding.

### Capabilities

- Matches scene descriptions in instructions (e.g., the word "bedroom") to the visual scene category.
- Produces scene‑level features that are fused with object‑level features from an object detector ⚠️ ⚠️ to create a unified multimodal representation.

### Relationships

- **part_of** → SOAT ⚠️ ⚠️ – Scene classification is an integral component of the SOAT multimodal architecture.
- **used_with** → object detector ⚠️ ⚠️ – The two visual encoders (scene classifier and object detector) operate in tandem; the scene classifier provides global context, while the object detector provides local, instance‑level details.

### Description

> Scene classification network used as one of two visual encoders in SOAT. It produces features that align with scene‑level cues in natural language instructions.

This approach is detailed in the paper *SOAT: Scene- and Object-Aware Transformer for Visual Grounding* (arXiv:2110.14143).

### Related Concepts

- Visual Grounding
- Embodied AI
- Object Detection
- Multimodal Learning ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Scene Classification` --related_to ⚠️--> `Embodied AI`
