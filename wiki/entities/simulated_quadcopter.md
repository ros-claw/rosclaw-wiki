---
id: simulated_quadcopter
title: Simulated Quadcopter
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:48:38'
last_reinforced: '2026-04-30T02:48:38'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

## Simulated Quadcopter

A **Simulated Quadcopter** is a virtual UAV platform used to evaluate the [[Grounded Semantic Mapping Network (GSMN)]] on high-level navigation instruction following tasks. It operates within realistic quadcopter simulators that emulate flight dynamics and sensor feedback.

### Capabilities

- Provides realistic simulation for testing [[navigation instruction following]] ⚠️ in virtual environments.
- Supports continuous low-level velocity control, enabling fine-grained movement commands during evaluation.

### Parameters

- **Environment**: Virtual environments with realistic quadcopter simulator.

### Relationships

- **Used by**: [[Grounded Semantic Mapping Network (GSMN)]] – this platform serves as the embodiment for evaluating the GSMN model’s ability to map natural language instructions to navigational actions.

### Source

- Original experiments described in arxiv paper [[papers/1806.00047.pdf]] ⚠️ (Grounded Semantic Mapping Network).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Simulated Quadcopter` --[[uses]] ⚠️--> `Grounded Semantic Mapping Network (GSMN)`
