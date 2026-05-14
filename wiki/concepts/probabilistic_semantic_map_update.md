---
id: probabilistic_semantic_map_update
title: Probabilistic-Semantic Map Update
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:00:44'
last_reinforced: '2026-04-30T00:00:44'
supersedes: []
sources:
- papers/2409.11764.pdf
source_type: arxiv_paper
---

# Probabilistic-Semantic Map Update

## Overview

**Probabilistic-Semantic Map Update** is a map representation ⚠️ technique that maintains a probability distribution over semantic classes for each cell in a spatial map. By storing per-cell class probabilities and updating them incrementally with new observations, this method mitigates the impact of noisy feature extraction ⚠️ ⚠️ and enables uncertainty-informed exploration.

## Details

- **Type**: Map representation update
- **Output**: semantic uncertainty ⚠️ used to guide exploration decisions
- **Key characteristic**: Instead of storing a single hard semantic label per map cell, the system maintains a probabilistic belief (e.g., a categorical distribution over possible object/region classes).

### Capabilities

- Reduces the negative effect of common errors in semantic feature extraction ⚠️ (e.g., misclassification due to lighting, occlusion, or viewpoint).
- Provides a quantified measure of semantic uncertainty per cell, which can be leveraged by an exploration planner to prioritize areas of high uncertainty.
- Enables robust long-term mapping in dynamic or ambiguous environments.

## Innovation

Uses probabilistic updates to maintain a distribution over semantic classes per map cell. This contrasts with deterministic label assignments that discard confidence information. Each new observation updates the cell's distribution using a Bayesian or evidence-based rule, allowing the map to naturally reflect ambiguity and to converge toward higher certainty as more data is collected.

## Relationships

- **Used by**: OneMap – This map representation is a core component of the OneMap system.
- **Depends on**: uncertainty estimation ⚠️, feature extraction ⚠️ ⚠️ – The update rule requires both a feature extraction pipeline that outputs class logits or confidence scores, and an uncertainty estimation mechanism (e.g., model uncertainty, aleatoric uncertainty).
- **Related concepts**: Occupancy Grid Map ⚠️, Semantic Mapping ⚠️, Exploration under Uncertainty ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Probabilistic-Semantic Map Update` --related_to ⚠️--> `OneMap` _(wikilink)_
