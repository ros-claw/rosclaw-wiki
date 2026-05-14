---
id: traveluav_benchmark
title: TravelUAV benchmark
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T20:53:54'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

# TravelUAV Benchmark

TravelUAV is a **benchmark dataset for unmanned aerial vehicle (UAV) navigation**, specifically designed for **aerial vision-language navigation (VLN)**. It provides a standardized evaluation framework for UAV navigation algorithms, incorporating dataset scaling across diverse reward settings to support long-horizon trajectory planning tasks.

## Description

TravelUAV addresses the challenge of navigating UAVs through complex environments using natural language instructions and visual observations. The benchmark offers multiple reward configurations and scales its dataset across diverse settings to test algorithm robustness across different environments and task complexities.

## Capabilities

- **Evaluation of UAV navigation algorithms** – Provides a unified metric suite for comparing VLN agents in aerial settings.
- **Support for long-horizon trajectory planning tasks** – Benchmark tasks require agents to plan and execute extended flight paths based on linguistic commands.

## Evaluation

Used to evaluate OpenVLN performance. Experiments are conducted with dataset scaling across diverse reward settings, assessing how well models generalize under varying conditions.

## Relationships

- Used by **OpenVLN** – The OpenVLN framework leverages TravelUAV for evaluating its aerial navigation models.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `TravelUAV benchmark` --uses ⚠️--> `OpenVLN`