---
id: hm3d_objnav
title: HM3D-ObjNav
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:49:06'
last_reinforced: '2026-04-30T03:49:06'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

# HM3D-ObjNav

**HM3D-ObjNav** is a benchmark for object navigation, built on the [[Habitat-Matterport 3D]] ⚠️ (HM3D) dataset. It evaluates an agent’s ability to locate and navigate to a specified object category in a realistic indoor environment, given only visual observations and a semantic target.

## Description

HM3D-ObjNav provides a standardized testbed for object goal navigation (ObjectNav) tasks. The benchmark uses high-fidelity 3D scans of real indoor spaces from the [[HM3D]] dataset and defines a set of object categories (e.g., chair, bed, TV) as goals. Agents must traverse the environment efficiently to reach the target object without a pre-built map.

The benchmark has been used to measure progress in embodied navigation research. Notably, the model [[MSGNav]] achieves state-of-the-art performance on HM3D-ObjNav, demonstrating superior scene understanding and long-horizon planning.

## Relationships

- **used to evaluate**: [[MSGNav]] – MSGNav reports top results on the HM3D-ObjNav benchmark.

## See also

- [[ObjectNav]] – The general task of object goal navigation.
- [[Habitat Platform]] ⚠️ – The simulator used to run HM3D-ObjNav episodes.
- [[Embodied AI]] – The broader research field.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HM3D-ObjNav` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `HM3D-ObjNav` --[[related_to]] ⚠️ ⚠️--> `MSGNav` _(wikilink)_
