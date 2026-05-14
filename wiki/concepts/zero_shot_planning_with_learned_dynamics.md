---
id: zero_shot_planning_with_learned_dynamics
title: Zero-shot planning with learned dynamics
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:05:39'
last_reinforced: '2026-04-30T04:05:39'
supersedes: []
sources:
- papers/2504.19322.pdf
source_type: arxiv_paper
---

# Zero-shot planning with learned dynamics

**Zero-shot planning with learned dynamics** is a paradigm in model-predictive control where a learned forward dynamics model is used to plan trajectories without requiring a hand-designed cost function or per-environment tuning. The planner operates heuristic-free, eliminating the need for environment-dependent reward shaping. This approach generalizes across environments without cost function redesign.

## Key characteristics

| Parameter | Value |
|-----------|-------|
| Heuristic-free | Yes |
| Environment-dependent tuning | Eliminated |

## Capabilities

* Generalizes across environments without cost function redesign

## Relationships

* **Implemented by**: Model Predictive Path Integral ⚠️ — this algorithm uses the learned dynamics to perform sampling-based optimization during planning.
* **Depends on**: Learned Perceptive Forward Dynamics Model — a neural dynamics model that takes observations and actions to predict future states, enabling the planner to reason about environment physics without explicit programming.

## Details

In traditional model-predictive control (MPC), a cost function must be carefully designed for each new environment to guide the planner toward desirable behavior. Zero-shot planning with learned dynamics removes this requirement by leveraging a learned model that implicitly captures task-relevant semantics from data. The planner (e.g., MPPI) can then be run directly without any environment-specific tuning, drastically reducing deployment effort. This technique is especially valuable in manipulation and locomotion tasks where dynamics vary across surfaces, objects, or terrains.

---

*Source: arxiv paper 2504.19322*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-shot planning with learned dynamics` --related_to ⚠️--> `Learned Perceptive Forward Dynamics Model` _(wikilink)_
