---
id: multi_modal_sequence_to_sequence_model
title: Multi-modal Sequence-to-Sequence Model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:24:24'
last_reinforced: '2026-04-29T21:24:24'
supersedes: []
sources:
- papers/1907.04957.pdf
source_type: arxiv_paper
---

## Multi-modal Sequence-to-Sequence Model

### Overview

A **Multi-modal Sequence-to-Sequence Model** is an Algorithm ⚠️ that combines Language ⚠️ ⚠️ and visual inputs to produce Navigation Actions ⚠️ ⚠️ conditioned on multi-turn Dialog History ⚠️. It extends the classic Sequence-to-Sequence Architecture ⚠️ ⚠️ by accepting multiple modalities and a longer temporal context.

### Parameters

| Parameter | Description |
|-----------|-------------|
| **lookback** | Longer dialog history improves Navigation ⚠️ performance. The model benefits from retaining extended conversation context. |
| **modalities** | Language ⚠️ ⚠️ (dialog turns) and Vision ⚠️ (visual observations or scene context) — implied from source. |

### Capabilities

- Reasoning over multi-turn dialog history to inform navigation decisions.
- Mapping from dialog and visual context to Navigation Actions ⚠️ ⚠️ (e.g., move, turn, go to location).

### Model

The authors establish an initial, multi-modal sequence-to-sequence model. They demonstrate that looking farther back in the dialog history improves performance. This finding suggests that richer temporal context from user instructions or clarifications is critical for robust embodied navigation.

### Relationships

- **Used in**: Navigation from Dialog History (task / application).
- **Depends on**: Sequence-to-Sequence Architecture ⚠️ ⚠️ (core backbone).
- **Related concepts**: Visual Grounding, Dialog State Tracking ⚠️, Goal-Oriented Dialogue ⚠️.

---

*See also: Attention Mechanism ⚠️, Transformer ⚠️, Encoders for Multi-Modal Data ⚠️*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multi-modal Sequence-to-Sequence Model` --based_on ⚠️ ⚠️--> `Embodied AI`
- `Multi-modal Sequence-to-Sequence Model` --based_on ⚠️ ⚠️--> `Navigation from Dialog History`
