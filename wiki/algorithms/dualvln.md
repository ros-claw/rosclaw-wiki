---
id: dualvln
title: DualVLN
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:51:30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# DualVLN

## Overview

**DualVLN** is a dual-system foundation model for vision-and-language navigation (VLN). It synergistically integrates high-level reasoning (System 2) with low-level action execution (System 1). The model is designed to deliver generalizable vision-language navigation, smooth trajectory generation, robust real-time control, adaptive local decision-making in complex dynamic environments, long-horizon planning, real-time adaptability, dynamic obstacle avoidance, and generalization across benchmarks and real-world settings. It supersedes traditional end-to-end VLN pipelines ⚠️ by decoupling global reasoning from local control.

## System 2 – Global Planner

System 2 is a **VLM-based global planner** that "grounds slowly". It uses Vision-Language Models ⚠️ ⚠️ (VLM) to predict mid-term waypoint goals via image-grounded reasoning. This component handles high-level reasoning and long-horizon planning, ensuring the agent understands the task and environment at a semantic level. By leveraging diverse vision-language data, System 2 retains strong generalization capabilities.

## System 1 – Local Planner

System 1 is a lightweight **multi-modal conditioning Diffusion Transformer ⚠️ ⚠️ policy** that "moves fast". It receives explicit pixel goals and latent features from System 2 and generates smooth, accurate trajectories in real time. This component handles low-level control, local navigation, and dynamic obstacle avoidance. Its architecture is interpretable and effective when trained on local navigation tasks.

## Dual-System Synergy

The two systems operate in a tightly coupled loop: System 2 "grounds slowly" by predicting mid-term waypoints through image-grounded reasoning, while System 1 "moves fast" by leveraging the explicit pixel goals and latent features from System 2 to execute precise local actions. This synergy enables both long-horizon planning and real-time adaptability in complex dynamic environments.

## Training Decoupling

The dual-system architecture decouples training for the two components. The VLM (System 2) retains its generalization capability by training on diverse vision-language data, while System 1 learns interpretable and effective local navigation through imitation learning or reinforcement learning conditioned on the goals provided by System 2. This decoupling ensures that neither component is a bottleneck, and the system as a whole benefits from the strengths of each.

## Capabilities

- Generalizable vision-language navigation
- Smooth trajectory generation
- Robust real-time control
- Adaptive local decision-making in complex dynamic environments
- Long-horizon planning
- Real-time adaptability
- Dynamic obstacle avoidance
- Generalization across benchmarks and real-world scenarios

## Relationships

- **Uses** → VLM-based Global Planner, Multi-modal Conditioning Diffusion Transformer Policy.
- **Depends on** → Vision-Language Models ⚠️ ⚠️, Diffusion Transformer ⚠️ ⚠️.
- **Implements** → Vision-Language Navigation task.
- **Supersedes** → End-to-End VLN Pipelines ⚠️.

### 自动链接关系  
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**
- `DualVLN` --extends ⚠️ ⚠️--> `VLM-based Global Planner`
- `DualVLN` --extends ⚠️ ⚠️--> `Multi-modal Conditioning Diffusion Transformer Policy`