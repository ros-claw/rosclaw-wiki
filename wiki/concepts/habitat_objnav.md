---
id: habitat_objnav
title: Habitat ObjNav
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:23:40'
last_reinforced: '2026-04-30T01:23:40'
supersedes: []
sources:
- papers/2406.04882.pdf
source_type: arxiv_paper
---

### Overview

**Habitat ObjNav** (Habitat Object Navigation) is a zero-shot object navigation benchmark within the [[Habitat Simulator]]. It evaluates an agent's ability to navigate to a specific object category in a previously unseen 3D environment, without any task‑specific training.

### Capabilities

- Tests object goal navigation in simulated 3D environments.
- Operates in a zero-shot setting—agents are not allowed to adapt or fine‑tune on the target layout.

### Description

Habitat ObjNav is a zero-shot object navigation task in the Habitat simulator. [[InstructNav]] surpasses the previous state‑of‑the‑art by **10.48%** on this benchmark (zero-shot variant).

### Relationships

- **used_by** – [[InstructNav]] uses [[Habitat ObjNav]] as an evaluation benchmark to measure navigation performance.
- **related_to** – Related navigation benchmarks include [[R2R-CE]] and [[DDN]].

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Habitat ObjNav` --[[applies_to]] ⚠️--> `R2R-CE`
