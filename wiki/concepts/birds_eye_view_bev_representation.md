---
id: birds_eye_view_bev_representation
title: Bird's-Eye-View (BEV) Representation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:44:13'
last_reinforced: '2026-04-30T01:44:13'
supersedes: []
sources:
- papers/2308.04758.pdf
source_type: arxiv_paper
---

# Bird's-Eye-View (BEV) Representation

**Bird's-Eye-View (BEV)** is a grid-level representation of the environment as seen from an overhead perspective. It encodes 3D scene geometry, captures spatial layouts and relationships, and reduces ambiguity in panoramic view selection. BEV representations are commonly used in autonomous driving ⚠️ ⚠️ and indoor navigation ⚠️ ⚠️ to provide geometric and semantic cues.

## Parameters

- **Type:** Grid-level representation
- **Scope:** Local per step and global with topological relations
- **Supervision:** 3D detection for geometric cues

## Capabilities

- Encodes 3D scene geometry
- Captures spatial layouts and relationships
- Reduces ambiguity in panoramic view selection

## Relationships

- **Used in:** BSG (BEV Scene Graph)
- **Related to:** autonomous driving ⚠️ ⚠️, indoor navigation ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Bird's-Eye-View (BEV) Representation` --related_to ⚠️--> `BSG (BEV Scene Graph)` _(wikilink)_
