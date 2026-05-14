---
id: foundational_models_in_robotics
title: Foundational models in robotics
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:02:18'
last_reinforced: '2026-04-30T04:02:18'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Foundational Models in Robotics

**Foundational models** refer to large-scale, pre-trained models (often vision-language models, such as CLIP, DINOv2, or GPT-4V) that provide rich representations and reasoning capabilities for perception and decision-making tasks. In robotics, these models enable **open-set visual perception and reasoning** — allowing a robot to interpret novel objects, scenes, and instructions without task-specific fine-tuning. They are commonly repurposed for downstream modalities including **depth estimation**, **traversability analysis**, and **goal generation**.

## Capabilities

- **Open-set visual perception and reasoning** — Foundational models can recognize and reason about unseen categories or environments by leveraging their broad pre-training dataset.
- **Depth estimation** — Many vision-based foundational models (e.g., DPT, MiDaS) can be adapted to produce metric or relative depth maps from a single image.
- **Traversability** — Outputs from foundational models (e.g., semantic segmentation, affordance maps) are used to predict which terrain or paths a robot can safely traverse.
- **Goal generation** — By integrating with large language or vision-language models, foundational models can propose navigation or manipulation goals based on high-level instructions or scene understanding.

## Relationships

- **Used by** TANGO — TANGO (the paper referenced from `papers/2509.08699.pdf`) leverages foundational models to achieve open-set generalization in robotic tasks such as traversability and goal generation. The exact implementation details are described in the TANGO page.

- **Depends on** Vision-Language Models ⚠️ ⚠️ and Large Pre-trained Backbones ⚠️ — Foundational models in robotics typically build on top of models like CLIP, DINOv2 ⚠️ ⚠️, or GPT-4V ⚠️ ⚠️.

- **Implements** Open-Set Perception ⚠️ ⚠️ — By nature, foundational models allow robots to operate outside closed-set assumptions.

## Usage Notes

When integrating foundational models into a robot’s software stack (e.g., in a ROS 2 ⚠️ node), careful consideration of computational cost, model latency, and environment-specific fine-tuning is necessary. Many implementations run the model on a separate GPU server and communicate via ROS 2 Topics ⚠️.

For a practical example, see the TANGO skill page which demonstrates how to wire up a foundational model for traversability and goal generation in real-time.

## Related Pages

- TANGO
- Open-Set Perception ⚠️ ⚠️
- Vision-Language Models ⚠️ ⚠️
- CLIP
- DINOv2 ⚠️ ⚠️
- GPT-4V ⚠️ ⚠️
- Depth Estimation (Algorithm) ⚠️
- Traversability (Concept) ⚠️
- Goal Generation (Concept) ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Foundational models in robotics` --related_to ⚠️ ⚠️--> `TANGO` _(wikilink)_
- `Foundational models in robotics` --related_to ⚠️ ⚠️--> `CLIP` _(wikilink)_
