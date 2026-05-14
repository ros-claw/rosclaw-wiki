---
id: cross_modal_matching_agent
title: Cross-Modal Matching Agent
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:09:58'
last_reinforced: '2026-04-30T02:09:58'
supersedes: []
sources:
- papers/2203.02764.pdf
source_type: arxiv_paper
---

# Cross-Modal Matching Agent

A **Cross-Modal Matching Agent** is a vision-and-language navigation (VLN) algorithm designed to navigate in Continuous Environments ⚠️ ⚠️ by aligning visual observations with natural language instructions. It operates by matching cross-modal information to decide high-level movement decisions, such as jumping from one navigable node to another.

## Overview

The agent relies on a Waypoints Predictor ⚠️ ⚠️ to convert low-level continuous states into discrete high-level action targets. This bridge between the discrete action space typical of pre-trained VLN models and the continuous physical world improves navigation robustness. In the paper from which this algorithm is derived (arXiv:2203.02764), the Cross-Modal Matching Agent demonstrates a **11.76% improvement in SPL** (Success weighted by Path Length) over baselines that do not use the waypoint predictor, effectively reducing the discrete-to-continuous gap.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `action_type` | High-level actions (node-to-node jumps) |

The agent outputs high-level actions that correspond to moving between predicted waypoints, rather than low-level motor commands. This abstraction allows it to leverage existing discrete VLN models with minimal modification.

## Capabilities

- Navigates in Continuous Environments ⚠️ ⚠️ using predicted waypoints as intermediate goals.
- Improves the discrete-to-continuous navigation gap by **11.76% SPL** relative to prior methods.

## Relationships

- **Uses** → Waypoints Predictor ⚠️ ⚠️: The agent depends on this module to generate reachable positions that define the high-level action targets.

## Related Concepts

- Vision-and-Language Navigation – the broader task domain.
- Sim-to-Real ⚠️ – continuous VLN often requires bridging simulation and real-world deployment.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Cross-Modal Matching Agent` --based_on ⚠️--> `Vision-and-Language Navigation`
