---
id: minivln
title: MiniVLN
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:49:58'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2409.18800.pdf
source_type: arxiv_paper
---

# MiniVLN

MiniVLN is a student model produced by progressive knowledge distillation, designed for efficient **Vision-and-Language Navigation (VLN)**. It maintains high performance while having only about 12% of the teacher model's parameters, making it well-suited for deployment on Embodied AI platforms with limited computational resources.

## Training Approach

The distillation is performed in two stages: first during pretraining to capture fine-grained knowledge, then during fine-tuning to capture navigation-specific knowledge. This two-stage approach is more effective than single-stage distillation in closing the performance gap.

## Capabilities

- **Vision-and-Language Navigation** – Efficiently interprets natural language instructions and visual observations to navigate in realistic environments.
- **Lightweight model suitable for Embodied AI platforms with limited computation** – Enables real-time navigation on resource-constrained hardware like mobile robots and drones.
- **Performance on par with teacher model** – Achieves comparable accuracy on standard VLN benchmarks despite the 88% reduction in parameters.

## Parameters

- **Parameter count**: ~12% of the teacher model.
- **Distillation method**: Two-stage knowledge distillation (`Two-Stage Knowledge Distillation`) – first during pretraining, then during fine-tuning.

## Relationships

- **uses**: Two-Stage Knowledge Distillation, Teacher Model ⚠️ ⚠️, knowledge distillation
- **depends_on**: Teacher Model ⚠️ ⚠️, Two-Stage Knowledge Distillation
- **implements**: Vision-and-Language Navigation

## Evaluation

MiniVLN has been evaluated on the standard VLN benchmarks:

- **R2R** – Room-to-Room navigation dataset.
- **REVERIE** – Remote Visual Embodied Referring Expression navigation.

Its performance on these benchmarks demonstrates that the distilled student model retains high navigation accuracy while drastically reducing model size.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MiniVLN` --based_on ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `MiniVLN` --based_on ⚠️ ⚠️--> `Two-Stage Knowledge Distillation`