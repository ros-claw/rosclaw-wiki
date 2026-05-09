---
id: dagger
title: DAgger
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:07:29'
last_reinforced: '2026-04-30T04:07:29'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

# DAgger

**DAgger** (Dataset Aggregation) is an **online imitation learning** algorithm designed to distill and aggregate expert policies into a robust student policy. It operates by iteratively collecting new trajectories from the current student policy, querying an expert for corrective actions on those states, and adding the resulting state‑action pairs to the training dataset. This closed‑loop interaction helps the student generalize beyond the static demonstration distribution.

## Parameters

| Attribute | Value |
|-----------|-------|
| Type | [[Imitation Learning]] (online, interactive) |
| Purpose | Distillation and aggregation of expert policies |
| Relationship | `implements` → [[Imitation Learning]] |

## Capabilities

- **Enable expert aggregation**: DAgger combines demonstrations from multiple experts or a single expert across diverse states encountered during rollouts.
- **Improve generalization**: By exposing the student to its own induced distribution, the policy learns to recover from errors and handle out‑of‑distribution states.

## Role in Framework

DAgger algorithm is used to distill multiple expert policies into a single **[[Foundation Policy]] ⚠️**. In this setting, each expert provides corrective feedback on states visited by the current policy, and the aggregated dataset trains a unified model that captures the strengths of all experts.

- `depends_on` → [[Expert Policies]] ⚠️ ⚠️ (source of corrective actions)
- `used_by` → [[Multi-expert Distillation]] (as a core mechanism for fusing multiple experts)

## Relationships

| Relation | Target | Description |
|----------|--------|-------------|
| `used_by` | [[Multi-expert Distillation]] | The Multi-expert Distillation framework employs DAgger to collect expert feedback across multiple domains. |
| `implements` | [[Imitation Learning]] | DAgger is a canonical example of interactive imitation learning. |
| `depends_on` | [[Expert Policies]] ⚠️ ⚠️ | Requires at least one expert to provide corrective actions during training. |

## Further Reading

- For a formal description, see the original DAgger paper (Ross et al., 2011).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `DAgger` --[[extends]] ⚠️--> `Multi-expert Distillation`
