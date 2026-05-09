---
id: baseline_controller
title: Baseline Controller
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:39:56'
last_reinforced: '2026-04-29T21:39:56'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Baseline Controller

The **Baseline Controller** is a fallback navigation mechanism used by the [[TANGO]] system. It activates when TANGO's local metric control fails or returns low-confidence predictions, providing a robust alternative to maintain robot mobility in uncertain environments.

## Overview

In the context of embodied navigation, local metric controllers can occasionally fail due to sensor noise, occlusions, or ambiguous terrain. The Baseline Controller serves as a safety net, taking over control to prevent collisions or getting stuck. It operates without relying on high-fidelity metric maps, instead using simpler heuristics or reactive behaviors.

## Capabilities

- **Fallback redundancy**: Provides navigation when [[TANGO]]'s local metric control is uncertain or fails.
- **Robustness**: Ensures the robot can continue moving even under degraded perception conditions.
- **Seamless switching**: Integrates with TANGO's decision pipeline to activate only when needed, without manual intervention.

## Relationships

- **Used by**: This controller is part of the [[TANGO]] system, which depends on it as a fallback module. `[[Baseline Controller]]` is *used by* `[[TANGO]]`.

## Related Concepts

- [[Local Metric Control]] ⚠️ — the primary navigation method that this controller replaces when uncertain.
- [[Embodied Navigation]] — broader field of robot movement in real-world environments.
- [[Fallback Behavior]] ⚠️ — design pattern for robust autonomy.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Baseline Controller` --[[uses]] ⚠️--> `TANGO`
