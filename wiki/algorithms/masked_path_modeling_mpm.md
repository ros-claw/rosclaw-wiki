---
id: masked_path_modeling_mpm
title: Masked Path Modeling (MPM)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:10:16'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2305.14268.pdf
source_type: arxiv_paper
---

# Masked Path Modeling (MPM)

**Masked Path Modeling (MPM)** is a self-supervised pretraining algorithm for **Vision-and-Language Navigation (VLN)**. During training, an agent collects paths by exploring environments without any specific goal. A random subpath is then masked, and the agent must reconstruct the original path from the visible context, thereby learning conditional action generation in a language-agnostic manner—all without requiring human annotations.

## Methodology

MPM pretrains an agent by randomly masking a subpath from a traversed trajectory and training the agent to reconstruct the full path. The agent explores environments without a goal, accumulating diverse data for pretraining.

### Parameters

- **Masking strategy**: Random subpath masking — a continuous segment of the trajectory is hidden.
- **Training objective**: Reconstruct the original path from the masked subpath (i.e., predict missing actions/waypoints).
- **Data collection**: Active exploration without a specific goal; the agent navigates freely to generate a diverse set of trajectories.

Formally, given a full path $\tau = (o_1, a_1, o_2, a_2, ..., o_T)$ where $o_t$ are observations and $a_t$ are actions, a subpath $\tau_{mask}$ is replaced with a mask token. The model learns $p(\tau_{mask} | \tau_{visible})$ via a cross-entropy loss over actions. This objective forces the agent to internalize spatiotemporal dependencies and navigation dynamics.

## Capabilities

- Improves success rate on VLN benchmarks.
- Enables conditional action generation from visual context.
- Allows self-supervised pretraining without human annotations.

## Results

MPM was evaluated on standard VLN benchmarks with the following improvements on **val-unseen splits**:

| Benchmark | Improvement over baseline |
|-----------|---------------------------|
| R2R       | +1.32%                    |
| R4R       | +1.05%                    |
| RxR       | +1.19%                    |

These gains demonstrate that self-supervised path reconstruction provides a useful inductive bias for generalization to unseen environments.

## Relationships

- **Used for**: [[Vision-and-Language Navigation]] (VLN) as the task domain.
- **Depends on**: [[agent exploration]] ⚠️ for unsupervised data collection; self-collected path data.
- **Related to**: Other self-supervised pretraining techniques for embodied agents, such as masked autoencoding.

## Source

This article is based on the arXiv paper *Masked Path Modeling for Vision-and-Language Navigation* (2023), arXiv:2305.14268.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Masked Path Modeling (MPM)` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`