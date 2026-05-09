---
id: gel_r2r
title: GEL-R2R
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:36:41'
last_reinforced: '2026-04-30T01:36:41'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

GEL-R2R is a grounded, entity-level annotation dataset derived from the [[R2R]] dataset. It augments the original VLN (Vision-and-Language Navigation) instructions with fine-grained, grounded entity–landmark human annotations, enabling cross-modal alignment pre-training at the entity level. GEL-R2R was introduced in the arxiv paper "2308.12587" and serves as the pre-training resource for the [[GELA]] ⚠️ ⚠️ model.

## Overview

GEL-R2R provides entity-level supervision for VLN models, bridging the gap between coarse instruction-following and fine-grained visual grounding. By annotating specific entities and landmarks mentioned in R2R instructions, GEL-R2R supports tasks requiring accurate referential grounding in 3D indoor environments.

## Parameters

- **Base dataset**: [[R2R]]
- **Annotation type**: Grounded entity–landmark human annotations
- **Purpose**: Fine-grained cross-modal alignment pre-training

## Capabilities

- Enables entity-level supervision for [[VLN models]] ⚠️, improving their ability to associate natural language references with specific visual entities in complex scenes.

## Relationships

- `derived_from`: [[R2R]] – GEL-R2R enriches the existing R2R dataset with additional grounding annotations.
- `used_by`: [[GELA]] ⚠️ ⚠️ – The GELA model pre-trains on GEL-R2R to achieve improved entity-level grounding and navigation performance.

## See Also

- [[VLN]] ⚠️ – Vision-and-Language Navigation task family
- [[Cross-modal Alignment]] – Underlying concept of aligning visual and language representations
- [[Entity Grounding]] ⚠️ – The specific capability enabled by GEL-R2R

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GEL-R2R` --[[related_to]] ⚠️--> `Cross-modal Alignment`
