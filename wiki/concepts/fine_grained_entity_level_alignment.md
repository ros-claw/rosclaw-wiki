---
id: fine_grained_entity_level_alignment
title: Fine-grained entity-level alignment
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:13:00'
last_reinforced: '2026-04-29T21:13:00'
supersedes: []
sources:
- papers/2308.12587.pdf
source_type: arxiv_paper
---

## Fine-grained Entity-Level Alignment (GELA)

**Fine-grained Entity-Level Alignment** is a [[concept]] ⚠️ in [[Vision-and-Language Navigation]] (VLN) that improves navigation performance by mapping specific entity phrases from natural language instructions to corresponding landmarks in the visual environment. Unlike global instruction alignment, GELA operates at the level of individual objects or spatial landmarks, enabling more precise grounding and robust decision-making.

### Capabilities

- Maps specific entity phrases (e.g., "the red chair", "the wooden table") to corresponding landmarks detected in the environment.
- Enhances navigation accuracy by resolving ambiguities that arise when instructions refer to distinct visual elements.

### Relationships

- **Depends on**: [[Grounded entity-landmark annotations]] ⚠️ – requires a dataset linking textual entities to visual landmarks for training or inference.

### Relevance

A novel aspect of GELA is its focus on fine-grained alignment, which improves VLN performance beyond what is achievable with global instruction alignment alone. By grounding each entity reference independently, the agent can disambiguate between similar landmarks and follow instructions more reliably in complex environments.

### Source

- arXiv paper: *[Your Source Title]* (2308.12587)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Fine-grained entity-level alignment` --[[related_to]] ⚠️--> `Vision-and-Language Navigation`
