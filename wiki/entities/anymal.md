---
id: anymal
title: ANYmal
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:36:02'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2504.19322.pdf
source_type: arxiv_paper
---

# ANYmal

**ANYmal** is a quadrupedal legged robot designed for navigating complex environments. It serves as the validation platform in the research on [[Learned Perceptive Forward Dynamics Model]] for safe navigation, as described in the source paper `papers/2504.19322.pdf`.

## Capabilities

- Navigates complex environments using a [[Learned Perceptive Forward Dynamics Model]].
- Demonstrates [[Sim-to-real transfer]] to bridge simulation and real-world performance.
- Employs [[Model Predictive Path Integral (MPPI)]] for motion planning and control.

## Relationships

- **uses** → [[Learned Perceptive Forward Dynamics Model]]
- **uses** → [[Model Predictive Path Integral (MPPI)]]
- **depends_on** → [[Sim-to-real transfer]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ANYmal` --[[uses]] ⚠️ ⚠️--> `Learned Perceptive Forward Dynamics Model`
- `ANYmal` --[[uses]] ⚠️ ⚠️--> `Model Predictive Path Integral (MPPI)`

---

_This page has been reinforced by source `papers/2504.19322.pdf`._