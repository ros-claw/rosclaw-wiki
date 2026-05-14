---
id: zero_shot_sim_to_real_transfer
title: Zero-Shot Sim-to-Real Transfer
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:32:36'
last_reinforced: '2026-04-29T21:32:36'
supersedes: []
sources:
- papers/2505.08712.pdf
source_type: arxiv_paper
---

# Zero-Shot Sim-to-Real Transfer

## Overview

**Zero-shot sim-to-real transfer** is a paradigm in embodied AI that enables a robot policy trained entirely in simulation to be deployed directly in the real world without any fine-tuning or additional real-world data collection. This approach dramatically reduces the cost and complexity of deploying learned controllers for physical robots.

## Domain and Method

Zero-shot sim-to-real transfer in this context is applied to the **navigation** domain. The method used is an **end-to-end learned policy** that leverages privileged information guidance — i.e., access to ground-truth state information during training that is not available at deployment time. The policy is trained fully in simulation but generalizes to diverse real-world environments without requiring any real-world adaptation.

## Capabilities

- Enables deployment in diverse real-world environments without real-world fine-tuning.

## Relationships

- **Used by**: Navigation Diffusion Policy (NavDP) — zero-shot sim-to-real transfer is a key enabler for NavDP’s ability to navigate dynamic open-world environments.
- **Depends on**: privileged information guidance — the policy learns to infer hidden real-world dynamics by being conditioned on privileged simulation states during training. This relationship is an implementation of @depends_on.

## Significance

Zero-shot sim-to-real transfer allows robots to navigate dynamic open-world environments directly from simulation training, reducing the need for costly real-world data collection and hyperparameter tuning. This makes scalable deployment of navigation policies more practical and accelerates the development of generalist mobile robots.

## References

- Source: `data/raw/papers/2505.08712.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-Shot Sim-to-Real Transfer` --related_to ⚠️--> `Navigation Diffusion Policy (NavDP)` _(wikilink)_
