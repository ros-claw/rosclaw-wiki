---
id: knowledge_distillation
title: Knowledge Distillation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:08:55'
last_reinforced: '2026-04-30T00:08:55'
supersedes: []
sources:
- papers/2409.18800.pdf
source_type: arxiv_paper
---

## Knowledge Distillation

**Knowledge Distillation** is a model compression technique where a smaller, faster "student" model learns to mimic the behavior of a larger, more capable "teacher" model. In the context of embodied AI, this enables the deployment of lightweight models with competitive performance on resource-constrained platforms such as robots or edge devices.

### Two-Stage Distillation

This [[paper]] ⚠️ (2409.18800) introduces a **progressive two-stage distillation** framework that significantly improves student performance compared to single-stage approaches:

1. **Pretraining Phase** – The student learns high-level visual-language representations from the teacher during the pretraining stage, capturing general semantic knowledge (e.g., object grounding, scene understanding).
2. **Fine-tuning Phase** – During task-specific fine-tuning, the student absorbs domain-specific navigation behavior from the teacher, acquiring skills needed for embodied tasks such as [[Visual Language Navigation]] ⚠️ (VLN).

This staged approach allows the student to first build a strong foundation and then refine task-specific policies, effectively narrowing the performance gap with the teacher.

### Capabilities

- Transfers knowledge from a **large teacher model** to a **compact student model**.
- Produces lightweight models that maintain competitive performance after distillation.
- Applicable to [[Embodied AI]] tasks (e.g., [[VLN]] ⚠️), where real-time inference on limited hardware is required.

### Relationships

- **[[MiniVLN]]** uses this progressive two-stage distillation to achieve efficient navigation.
- Related concepts: [[model compression]] ⚠️, [[lightweight models]] ⚠️.
- Implements a form of [[transfer learning]] ⚠️ and is commonly paired with [[knowledge distillation]] variants (e.g., logit‑based, feature‑based).
- Depends on the availability of a pre‑trained teacher model for both stages.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Knowledge Distillation` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Knowledge Distillation` --[[related_to]] ⚠️ ⚠️--> `MiniVLN` _(wikilink)_
