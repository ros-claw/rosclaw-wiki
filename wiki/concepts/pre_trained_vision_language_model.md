---
id: pre_trained_vision_language_model
title: Pre-trained vision-language model
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:37:49'
last_reinforced: '2026-04-30T04:37:49'
supersedes: []
sources:
- papers/2312.03275.pdf
source_type: arxiv_paper
---

## Pre-trained Vision-Language Model

A **pre-trained vision-language model (VLM)** is a neural network trained on large-scale image-text pairs to learn a shared embedding space between visual and linguistic modalities. These models enable semantic grounding, allowing robotic systems to associate high-level language instructions with perceptual observations without task-specific fine-tuning.

### Description
A model (e.g., [[CLIP]], [[ALIGN]] ⚠️) pre-trained on millions of image-text pairs to understand semantic relationships between visual and linguistic inputs. This joint representation serves as the backbone for downstream tasks in embodied AI, including object detection, navigation instruction following, and task planning.

### Capabilities
- **Associate visual observations with semantic categories** &mdash; maps raw camera or depth data into a feature space aligned with natural language labels.
- **Zero-shot transfer to novel tasks** &mdash; the model generalizes to unseen objects, environments, or commands without additional training, enabling quick adaptation in robotics.

### Relationships
- **used_by**: [[VLFM]] (Vision-Language Frontier Maps) and [[Language-grounded value map]] rely on a pre-trained VLM to project visual features into semantic reward functions or navigation costmaps.
- **depends_on**: The utility of a VLM depends on the diversity and quality of the [[Contrastive Learning|contrastive learning]] objective used during pre-training.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Pre-trained vision-language model` --[[related_to]] ⚠️--> `CLIP` _(wikilink)_
