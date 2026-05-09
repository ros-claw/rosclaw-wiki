---
id: system_1
title: System 1
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:23:29'
last_reinforced: '2026-04-30T00:23:29'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# System 1

**System 1** is the **local motion controller** component within the [[DualVLN]] architecture. It is implemented as a **lightweight multi-modal conditioning Diffusion Transformer policy** that translates high-level navigation intent into smooth, executable trajectories.

## Input

System 1 accepts two types of input:
- **Explicit pixel goals** — visual targets derived from the environment.
- **Latent features** from [[System 2]] — the higher-level reasoning module that provides task context and subgoal planning.

## Capabilities

- **Smooth trajectory generation** — outputs continuous, kinematically feasible motion commands.
- **Fast action execution** — designed for low-latency control suitable for real-time robotic deployment.
- **Interpretable local navigation** — because it operates on explicit goals (e.g., pixel targets), its behavior is more transparent than end-to-end black-box policies.

## Relationships

- **Part of**: [[DualVLN]] — System 1 forms the lower‑level motion layer of the dual-system visual language navigation framework.
- **Depends on**: [[System 2]] — System 1 relies on System 2 for task decomposition, global planning, and latent features that condition its policy.
- **Uses**: [[Diffusion Transformer]] ⚠️ — the underlying generative model architecture for trajectory prediction.

## Source

- *arXiv:2512.08186* (2025) — Original paper introducing the DualVLN framework.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `System 1` --[[uses]] ⚠️--> `DualVLN`
