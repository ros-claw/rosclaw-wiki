---
id: reverie_benchmark
title: REVERIE benchmark
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-30T00:12:51'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2409.18800.pdf
- papers/2207.11201.pdf
source_type: arxiv_paper
---

# REVERIE Benchmark

The **REVERIE benchmark** (Remote Embodied Visual Referring Expression with Indirect Evaluation) is a public benchmark for evaluating **[[Vision-and-Language Navigation]] (VLN)** agents. It provides a standardized framework to test how well agents can follow natural language instructions to navigate through photorealistic environments, specifically focusing on locating remote objects or rooms described by referring expressions.

## Overview

REVERIE emphasizes the ability of agents to comprehend complex instructions that refer to distant targets, requiring both instruction understanding and spatial reasoning. Unlike simpler VLN tasks, the agent must navigate to an object or room that is not directly visible from the start location, demanding longer-horizon planning and robust environment grounding.

## Capabilities

- Evaluates **[[vision-and-language navigation]] agents** on their ability to interpret natural language commands and execute sequential navigation actions.
- Tests agents on navigating to remote locations described by natural language expressions, moving beyond short-range instructions to a more challenging setting.
- Designed for public use, allowing reproducible comparisons across different models and approaches.

## Relationships

- **evaluates** → [[MiniVLN]]: The [[MiniVLN]] model is evaluated on the REVERIE benchmark.
- **evaluates** → teacher model: A teacher model used for knowledge distillation or imitation learning is also evaluated on this benchmark.
- **used_by** → [[Target-Driven Structured Transformer Planner (TD-STP)]]: The TD-STP method is evaluated on the REVERIE benchmark.

## Usage

Researchers use the REVERIE benchmark to compare the performance of VLN agents, typically measuring success rate (SR), navigation error (NE), and other task-specific metrics. It serves as a standard testbed for advancing embodied AI research in the VLN domain, especially for tasks requiring indirect reference resolution and long-horizon navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `REVERIE benchmark` --[[related_to]] ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `REVERIE benchmark` --[[related_to]] ⚠️ ⚠️--> `vision-and-language navigation`
- `REVERIE benchmark` --[[uses]] ⚠️--> `MiniVLN`