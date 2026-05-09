---
id: uav
title: UAV
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T20:43:32'
last_reinforced: '2026-04-29T20:43:32'
supersedes: []
sources:
- papers/2512.15258.pdf
source_type: arxiv_paper
---

A **UAV** (Unmanned Aerial Vehicle) is a robotic aircraft operated without a human pilot onboard. In the context of embodied AI, UAVs serve as mobile platforms for autonomous navigation, perception, and interaction tasks, often constrained by limited computational resources and strict real‑time requirements.

## Capabilities

- **Real‑time onboard inference**: The UAV can process sensor data (e.g., camera, LiDAR) and run neural network models directly on its embedded computer without relying on cloud or off‑board compute.
- **Resource‑constrained computation**: The UAV operates under tight power, memory, and thermal budgets, requiring efficient algorithms and lightweight model architectures (e.g., quantized or distilled networks).

## Relationships

- **Runs**: The UAV runs **[[VLA-AN]]** (Vision‑Language‑Action Autonomous Navigation), a model that integrates visual perception, natural language understanding, and action generation for closed‑loop control.

> [!note]
> These capabilities are derived from the paper *[10.48550/arXiv.2512.15258]* which evaluates VLA‑AN deployment on a UAV with an onboard GPU (e.g., NVIDIA Jetson). The platform’s resource constraints inform the design of the VLA‑AN architecture (see [[VLA-AN#Onboard Deployment]] ⚠️).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `UAV` --[[uses]] ⚠️--> `VLA-AN`
