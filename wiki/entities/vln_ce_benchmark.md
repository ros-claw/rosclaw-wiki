---
id: vln_ce_benchmark
title: VLN-CE benchmark
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-30T00:20:54'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.17221.pdf
- papers/2507.05240.pdf
source_type: arxiv_paper
---

# VLN-CE Benchmark

The **VLN-CE (Vision-Language Navigation in Continuous Environments)** benchmark is a standard evaluation framework for assessing the performance of continuous vision-language navigation agents. Unlike discrete grid-based environments, VLN-CE simulates realistic, continuous 3D spaces where agents must execute natural language instructions by moving freely through the environment.

## Overview

VLN-CE was introduced to bridge the gap between simulated discrete navigation and real-world robot navigation. It measures an agent's ability to understand human instructions, perceive the environment, and plan continuous trajectories. The benchmark provides standardized datasets, evaluation metrics, and simulation environments.

## Capabilities

- Standard benchmark for evaluating continuous VLN agents
- Supports agents that operate in realistic 3D spaces with continuous action spaces
- Includes metrics such as success rate, navigation error, and path length
- Used to evaluate Vision-and-Language Navigation in continuous environments across diverse methods and architectures

## Evaluation Scope

The VLN-CE benchmark evaluates a wide range of continuous navigation agents. Beyond individual agents, it serves as a common testbed for comparing different VLN methods, providing a consistent framework that isolates navigation performance from environmental assumptions.

## Relationships

- **Evaluates**: [[VLN-R1]] – the benchmark is used to assess the VLN-R1 agent's performance in continuous environments.
- **Evaluates**: [[StreamVLN]] – the benchmark is used to evaluate StreamVLN’s ability to handle real-time continuous navigation.
- **Evaluates**: [[VLN methods]] ⚠️ – the benchmark serves as the primary evaluation platform for comparing the effectiveness of various VLN approaches in realistic, continuous settings.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLN-CE benchmark` --[[uses]] ⚠️--> `VLN-R1`
- `VLN-CE benchmark` --[[evaluates]] ⚠️ ⚠️--> `StreamVLN`
- `VLN-CE benchmark` --[[evaluates]] ⚠️ ⚠️--> `VLN methods`