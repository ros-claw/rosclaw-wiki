---
id: open_set_navigation
title: Open-set navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:01:37'
last_reinforced: '2026-04-30T04:01:37'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Open-set Navigation

**Open-set navigation** refers to the ability of a robotic system to navigate in environments containing previously unseen objects and scene configurations without requiring task-specific fine-tuning. Instead of relying on a closed set of known object classes or pre-mapped landmarks, open-set navigation leverages large-scale foundational models (e.g., vision-language models, segmentation models) to generalize across novel visual inputs. This paradigm is critical for deploying robots in unstructured, real-world settings where the full range of perceivable entities cannot be enumerated in advance.

## Capabilities

- **Operates on novel objects and scenes without fine-tuning** — The system can avoid, approach, or interact with objects it has never encountered during training, adapting on the fly through zero-shot generalization.
- **Leverages foundational models for generalization** — Pre-trained models (e.g., CLIP, SAM, DINOv2) provide semantic and geometric understanding that transfers to unseen domains, reducing the need for domain-specific data collection.

## Relationship

- **used_by** → TANGO: The TANGO system implements an open-set navigation pipeline that combines language-conditioned affordance prediction with real-time perception, enabling navigation in environments with unknown obstructions and dynamic targets.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Open-set navigation` --related_to ⚠️--> `TANGO` _(wikilink)_
