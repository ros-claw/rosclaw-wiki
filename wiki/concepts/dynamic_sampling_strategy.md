---
id: dynamic_sampling_strategy
title: Dynamic Sampling Strategy
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:40:10'
last_reinforced: '2026-04-30T00:40:10'
supersedes: []
sources:
- papers/2509.12129.pdf
source_type: arxiv_paper
---

# Dynamic Sampling Strategy

The **Dynamic Sampling Strategy** is a technique for controlling the number of observation tokens consumed by a model at inference time, subject to a **[[token length budget]] ⚠️**. By dynamically adjusting how many tokens are sampled for each observation, the strategy reduces computational load while preserving task performance, making it suitable for real-time or resource-constrained deployment.

## Parameters

- **token_length_budget**: *limited (unspecified)* — the maximum amount of tokens the model is allowed to spend on observations. The specific value is left as a deployment-dependent hyperparameter.

## Capabilities

- Controls the number of observation tokens to meet deployment constraints.
- Enables a trade-off between computational efficiency and model accuracy.

## Relationships

| Relation | Entity | Description |
|----------|--------|-------------|
| `used_by` | [[NavFoM]] | The NavFoM system incorporates this strategy to stay within inference budgets. |
| `purpose` | — | Reduce computational load while maintaining performance. |

## Method

Observation tokens are dynamically adjusted under a token length budget to balance efficiency and accuracy. The strategy decides at runtime how many tokens to retain from each observation, discarding or compressing the rest, so that the total token count never exceeds the budget. This allows the model to allocate tokens more intelligently (e.g., prioritizing informative regions) rather than using a fixed number.

## Source

- Based on *arxiv paper* `2509.12129.pdf`.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Dynamic Sampling Strategy` --[[related_to]] ⚠️--> `NavFoM` _(wikilink)_
