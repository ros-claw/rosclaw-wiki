---
id: panoramic_scene_parsing
title: Panoramic Scene Parsing
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:08:08'
last_reinforced: '2026-04-30T00:08:08'
supersedes: []
sources:
- papers/2511.06840.pdf
source_type: arxiv_paper
---

# Panoramic Scene Parsing

**Panoramic Scene Parsing** is a technique for extracting spatial layout information from full 360-degree panoramic RGB images. It serves as a critical perception module for embodied agents navigating in complex environments, providing a bird's-eye understanding of the scene structure that traditional narrow-field-of-view parsers cannot capture.

## Function

The primary function of Panoramic Scene Parsing is to extract spatial layout from 360-degree camera input to inform navigation decisions. By processing equirectangular or cubemap representations, it reconstructs floorplans, wall boundaries, obstacle positions, and free-space regions. This parsed scene representation is then used as a geometric context for path planning and goal reasoning.

## Capabilities

- **Unlocks spatial parsing potential of Multimodal Large Language Models (MLLMs):** By converting panoramic visual data into structured geometric representations, it enables MLLMs to reason about large-scale environments that extend beyond a single viewport. This capability allows language-guided navigation policies to incorporate holistic spatial awareness.

## Relationships

- **Used by [[PanoNav]]** – The PanoNav navigation system depends on Panoramic Scene Parsing to provide a global scene understanding from a single 360° image. PanoNav (uses) the parsed layout to fuse with additional sensors and plan collision-free trajectories.

## Dependencies

- Requires **Panoramic RGB images** as input (equirectangular or cubemap format).
- Typically relies on deep neural architectures (e.g., CNNs, transformers) trained on panoramic scene datasets.

## Sources

- `data/raw/papers/2511.06840.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Panoramic Scene Parsing` --[[related_to]] ⚠️--> `PanoNav` _(wikilink)_
