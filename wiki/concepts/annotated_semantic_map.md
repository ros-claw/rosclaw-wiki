---
id: annotated_semantic_map
title: Annotated Semantic Map
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:57:48'
last_reinforced: '2026-04-29T20:57:48'
supersedes: []
sources:
- papers/2502.13451.pdf
source_type: arxiv_paper
---

# Annotated Semantic Map (ASM)

## Overview

The **Annotated Semantic Map** (ASM) is a memory representation used within the MapNav architecture. Unlike traditional sequential memory (e.g., historical frame stacks), the ASM constructs a top-down semantic map that is updated at every timestep. Each key region of the map is annotated with explicit textual labels, enabling precise object mapping, structured navigation information, and clear navigation cues for an embodied agent.

## Components

| Component | Description |
|-----------|-------------|
| **Top‑down semantic map** | A bird’s‑eye view representation that encodes object locations, spatial layout, and semantic categories. |
| **Explicit textual labels** | Human‑readable tags (e.g., “chair”, “door”, “kitchen”) attached to map regions, providing natural language grounding for the agent’s decision‑making. |
| **Per‑timestep update** | The map is refreshed every timestep, incorporating new sensory observations and discarding outdated information. |

## Capabilities

- **Precise object mapping** – The ASM maintains an accurate inventory of objects and their positions in the environment.
- **Structured navigation information** – It provides a compact, semantically‑rich representation of the space, allowing the agent to plan paths and avoid obstacles.
- **Clear navigation cues** – Textual labels directly inform the agent where to go (e.g., “go to the table”) without requiring complex parsing of raw sensor data.

## Role in MapNav Architecture

The Annotated Semantic Map is a core component of the MapNav system. It replaces the historical frame sequences used in prior vision‑language navigation methods. By storing a top‑down semantic map with explicit labels, the ASM simplifies the mapping from perception to action, reducing the need for recurrent memory and enabling more interpretable navigation decisions.

The map is produced by a semantic segmentation module (Semantic Segmentation ⚠️ →) and consumed by the navigation policy (MapNav Policy ⚠️), which uses the textual labels to issue low‑level movement commands.

## Related Concepts

- MapNav – The navigation framework that leverages the ASM.
- Top‑down Semantic Map ⚠️ – A more general category of spatial representations; the ASM is a specific instantiation with textual annotations.
- Embodied Navigation – The broader domain in which ASM operates.
- Language‑Guided Navigation ⚠️ – The setting that motivates the use of explicit textual labels.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Annotated Semantic Map` --related_to ⚠️--> `MapNav` _(wikilink)_
