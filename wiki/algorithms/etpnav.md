---
id: etpnav
title: ETPNav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:02:17'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# ETPNav

## Overview
**Evolving Topological Planning for Vision-Language Navigation in Continuous Environments (ETPNav)** is a framework for **vision-language navigation** in continuous environments. It performs online topological mapping by clustering waypoints along the traversed path **without prior environmental experience**, enabling hierarchical planning. The framework decomposes the navigation task into high-level planning and low-level control, achieving state-of-the-art performance on standard benchmarks.

## Method
ETPNav consists of two main components:
- **[[Transformer-based Cross-modal Planner]]**: a high-level planner that generates long-range navigation plans by attending over topological maps and natural language instructions.
- **[[Obstacle-avoiding Controller]]**: a low-level controller that uses a [[Trial-and-error Heuristic]] ⚠️ ⚠️ to prevent the agent from getting stuck in local obstacles during continuous execution.

The system builds an online topological map by self-organizing predicted waypoints along the agent’s path, allowing it to abstract environments and plan over longer horizons.

## Results
ETPNav achieves state-of-the-art performance on both the [[R2R-CE dataset]] and [[RxR-CE dataset]] ⚠️ ⚠️:
- **R2R-CE**: >10% improvement over prior SOTA.
- **RxR-CE**: >20% improvement over prior SOTA.

## Parameters
| Parameter | Value |
|-----------|-------|
| Type | Vision-language navigation framework for continuous environments |
| Improvement over SOTA (R2R-CE) | >10% |
| Improvement over SOTA (RxR-CE) | >20% |
| Code | [https://github.com/MarSaKi/ETPNav](https://github.com/MarSaKi/ETPNav) |

## Capabilities
- Online topological mapping of environments by self-organizing predicted waypoints **without prior environmental experience**
- Break down navigation into high-level planning and low-level control
- Long-range navigation planning
- Obstacle avoidance via trial-and-error heuristic
- Cross-modal planning using a transformer-based planner

## Relationships
- **uses** [[Topological Mapping]]
- **uses** [[Transformer-based Cross-modal Planner]]
- **uses** [[Obstacle-avoiding Controller]]
- **uses** [[Trial-and-error Heuristic]] ⚠️ ⚠️
- **depends_on** [[Vision-Language Navigation in Continuous Environments (VLN-CE)]] ⚠️
- **depends_on** [[Transformer architecture]] ⚠️
- **evaluated_on** [[R2R-CE dataset]]
- **evaluated_on** [[RxR-CE dataset]] ⚠️ ⚠️

## Code
The open-source implementation is available at [https://github.com/MarSaKi/ETPNav](https://github.com/MarSaKi/ETPNav).