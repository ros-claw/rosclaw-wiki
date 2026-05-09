---
id: multi_modal_3d_scene_graph_m3dsg
title: Multi-modal 3D Scene Graph (M3DSG)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:31:55'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

# Multi-modal 3D Scene Graph (M3DSG)

A **Multi-modal 3D Scene Graph (M3DSG)** is a knowledge representation that extends traditional [[3D scene graph]] ⚠️ ⚠️ ⚠️s by preserving **visual cues** rather than compressing them into purely textual relational edges. In standard scene graphs, relationships between objects (e.g., “on top of”, “next to”) are encoded as text labels, which abstract away the rich visual detail of the real scene. M3DSG replaces these textual edges with **dynamically assigned images**, maintaining the original visual evidence (e.g., an image patch showing the actual spatial relationship) for each relation. This enables downstream tasks — such as querying or reasoning about the scene — to leverage full multimodal context instead of relying on abstracted text.

## Description

M3DSG is a novel representation that keeps visual information by using images as edge labels instead of text. This reduces construction cost and avoids irreversible loss of visual evidence. By attaching image-based evidence directly to each relational edge, M3DSG preserves fine-grained appearance, texture, and layout information that would otherwise be lost in a purely symbolic graph.

## Capabilities

- **Preserves visual evidence** – replaces textual relational edges with dynamically assigned images, keeping the original perceptual context for each relationship.
- **Enables open vocabulary reasoning** – because visual cues are retained, queries and reasoning can leverage the full multimodal context without being limited by a fixed set of textual relation labels.

## Relationships

- **uses**: [[3D scene graph]] ⚠️ ⚠️ ⚠️
- **used_by**: [[MSGNav]]
- **related_to**: [[3D scene graph]] ⚠️ ⚠️ ⚠️
- **depends_on**: none