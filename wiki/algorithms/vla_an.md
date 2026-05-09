---
id: vla_an
title: VLA-AN
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:43:06'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2512.15258.pdf
- papers/2512.15258.json
source_type: arxiv_paper
---

# VLA-AN

VLA-AN is an efficient onboard **Vision-Language-Action (VLA)** framework for autonomous drone navigation in complex environments. It addresses key limitations such as the domain gap between simulation and reality, insufficient temporal navigation reasoning, safety risks of generative action policies, and onboard deployment constraints on resource‑constrained [[UAV]] platforms. By integrating [[3D Gaussian Splatting]]‑based scene representation, a [[Progressive Three‑Stage Training Framework]] ⚠️ ⚠️ ⚠️, and a [[Geometric Safety Correction Module]] ⚠️ ⚠️ ⚠️, VLA‑AN achieves collision‑free, stable command generation with state‑of‑the‑art performance in spatial grounding, scene reasoning, and long‑horizon navigation.

## Capabilities

- Autonomous drone navigation in complex environments
- Spatial grounding of natural language instructions to 3D space
- Scene reasoning for obstacle avoidance and path planning
- Long‑horizon navigation with sustained stability
- Collision‑free and stable command generation
- Real‑time onboard inference
- Full‑chain closed‑loop autonomy

## Parameters

| Parameter | Value |
|-----------|-------|
| Architecture | Vision‑Language‑Action |
| Inference throughput improvement (vs. baseline) | 8.3× |
| Maximum single‑task success rate | 98.1% |

## Dataset Generation

VLA‑AN constructs a **high‑fidelity dataset** using [[3D Gaussian Splatting]] (3D‑GS) to bridge the domain gap between simulation and real‑world deployment. This dataset provides rich, grounded scene representations that enable the model to learn robust navigation policies from limited real‑world data.

## Training Framework

The [[Progressive Three‑Stage Training Framework]] ⚠️ ⚠️ ⚠️ sequentially reinforces three core competencies:

1. **Scene Comprehension** – Ground language understanding to 3D Gaussian representations.
2. **Core Flight Skills** – Train stable low‑level control policies.
3. **Complex Navigation Capabilities** – End‑to‑end integration for long‑horizon tasks.

## Action Module and Safety

A **lightweight real‑time action module** converts the trained model’s outputs into collision‑free commands. It integrates a [[Geometric Safety Correction Module]] ⚠️ ⚠️ ⚠️ that operates in the loop, applying real‑time geometric constraints to mitigate the stochastic nature of generative policies. This enables fast, stable decision‑making and ensures that commands remain dynamically feasible.

## Onboard Deployment Optimization

Through deep optimization of the [[Onboard Deployment Pipeline]] ⚠️, VLA‑AN achieves an **8.3× improvement in inference throughput** on resource‑constrained UAV hardware, making real‑time deployment feasible without sacrificing performance.

## Limitations Addressed

VLA‑AN tackles four principal limitations identified in prior VLA‑based navigation:

- **Data Domain Gap**: Mitigated through a high‑fidelity 3D‑GS dataset that aligns simulation with real‑world visual conditions.
- **Insufficient Temporal Navigation Reasoning**: Addressed by the progressive training framework and long‑horizon reasoning capabilities.
- **Safety Risks of Generative Action Policies**: Handled via the real‑time geometric safety correction module.
- **Onboard Deployment Constraints**: Overcome by deep pipeline optimization yielding 8.3× throughput gains on UAV hardware.

## Relationships

- **Uses**: [[3D Gaussian Splatting]] (3D‑GS), [[Progressive Three‑Stage Training Framework]] ⚠️ ⚠️ ⚠️, [[Geometric Safety Correction Module]] ⚠️ ⚠️ ⚠️, [[Onboard Deployment Pipeline Optimization]]
- **Depends on**: Lightweight action module, high‑fidelity dataset from 3D‑GS, [[Vision‑Language‑Action]] ⚠️ (VLA) architecture
- **Platform**: Lightweight aerial robots ([[UAV]])

## Source

- Paper: `data/raw/papers/2512.15258.pdf` (arXiv:2512.15258)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLA-AN` --[[extends]] ⚠️--> `3D Gaussian Splatting`
- `VLA-AN` --[[implements]] ⚠️--> `UAV`
**Pending review:**
- `VLA-AN` --[[related_to]] ⚠️--> `Onboard Deployment Pipeline Optimization` _(wikilink)_