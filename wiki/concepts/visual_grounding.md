---
id: visual_grounding
title: Visual Grounding
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:03:47'
last_reinforced: '2026-04-30T03:03:47'
supersedes: []
sources:
- papers/2004.14973.pdf
source_type: arxiv_paper
---

# Visual Grounding

## Overview

**Visual Grounding** is the ability to map textual references (e.g., "stairs") to corresponding regions in an image, i.e., to associate language expressions with specific visual content in the environment. This capability is fundamental for allowing embodied agents to interpret natural language commands in the context of their sensory input.

Visual grounding bridges the gap between perception and language, enabling robots to understand phrases like "the red chair to the left of the table" and locate the referenced object in the camera feed. It is a core component of many navigational and manipulation tasks where language serves as the primary interface.

## Capabilities

- **Link language references to visual content in the environment** – given a natural language phrase or description, identify the bounding box, segmentation mask, or keypoint set that corresponds to the described entity or spatial relation.

## Usage in Embodied AI

[[Visual Grounding]] is used by:

- [[Vision-and-Language Navigation (VLN)]] ⚠️ – agents must follow natural language instructions by grounding each instruction step to visual landmarks.
- [[VLN-BERT]] – a transformer-based architecture that explicitly models the alignment between language tokens and visual features for grounded navigation decisions.

## Related Concepts

- [[Embodied AI]] – the broader field where visual grounding enables situated reasoning.
- [[Semantic Segmentation]] ⚠️ – often used as a stepping stone for grounding object categories.
- [[Referring Expression Comprehension]] ⚠️ – a specific instance of visual grounding that resolves referring expressions.

## References

- Paper: *"VLN-BERT: A Recurrent Vision-and-Language BERT for Navigation"* (arXiv:2004.14973, 2020) - describes visual grounding as a core capability for VLN and presents model architecture that jointly learns grounding and navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visual Grounding` --[[related_to]] ⚠️--> `Embodied AI`
