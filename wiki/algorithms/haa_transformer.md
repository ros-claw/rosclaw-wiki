---
id: haa_transformer
title: HAA-Transformer
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:08:39'
last_reinforced: '2026-04-29T21:08:39'
supersedes: []
sources:
- papers/2205.12219.pdf
source_type: arxiv_paper
---

# HAA-Transformer

**Definition:** The HAA-Transformer (Human Attention Augmented Transformer) is a neural architecture that integrates human attention predictions into a transformer model for the task of **[[Aerial Vision-and-Dialog Navigation]] ⚠️ ⚠️**. It jointly predicts navigation waypoints and human attention maps from a history of dialog utterances and visual observations.

---

## Architecture

The model extends a standard transformer backbone by adding a **human attention module** that estimates which regions of the visual input a human operator would focus on during the navigation task. This attention prediction is fused with the visual and dialog features to improve waypoint prediction accuracy.

- **Parameters:**
  - `model_type`: Transformer with human attention integration

---

## Capabilities

- Predicts navigation waypoints from [[Dialog History]] ⚠️ in a continuous visual environment.
- Predicts human attention on visual observations, enabling the system to align its decision-making with human saliency.

---

## Relationships

- **used_for:** [[Aerial Vision-and-Dialog Navigation]] ⚠️ ⚠️
- **depends_on:** [[Vision-and-Language Navigation]] and [[Human Attention Modeling]] ⚠️ ⚠️

The HAA-Transformer builds upon prior work in [[Vision-and-Language Navigation]] by adding a task-specific dialog understanding component, and it incorporates techniques from [[Human Attention Modeling]] ⚠️ ⚠️ to generate attention maps that guide the spatial reasoning.

---

## Notes

- Presented in arxiv paper 2205.12219.
- Currently unverified in ROSClaw; confidence level set to 0.8 (peer-reviewed paper source).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HAA-Transformer` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
