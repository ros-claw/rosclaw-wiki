---
id: ascent
title: ASCENT
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:44:16'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

# ASCENT

**ASCENT** is an online framework for Zero-Shot Object-Goal Navigation that enables robots to navigate multi-floor buildings without pre-built maps or retraining on new object categories. The system combines a Multi-Floor Abstraction module with Coarse-to-Fine Reasoning to achieve floor-aware, staircase-adaptive exploration in real-world environments.

## Overview

ASCENT operates as an online, zero-shot navigation algorithm. It does not require prior mapping of the environment nor fine-tuning on novel object categories. The framework relies on Large Language Models (LLM ⚠️ ⚠️) for contextual analysis, uses **Frontier Ranking** to prioritize exploration frontiers, and employs stair-aware obstacle mapping and cross-floor topology modeling to handle multi-level buildings. Its coarse-to-fine exploration strategy allows efficient search over both global floor layout and local object targets.

## Capabilities

- Navigate multi-floor buildings
- Zero-shot object-goal navigation without pre-built maps
- Operate without retraining on new object categories
- Stair-aware obstacle mapping
- Cross-floor topology modeling
- LLM-driven contextual analysis
- Coarse-to-fine exploration
- Cross-floor transition support
- Real-world deployment on quadruped robot

## Architecture

ASCENT is composed of two main modules:

- **Multi-Floor Abstraction Module** – Models floor boundaries, stair connections, and cross-floor topology to build a compact representation of the building structure.
- **Coarse-to-Fine Reasoning Module** – First performs global floor-level search using LLM-derived context, then refines to local object search via zero-shot object-Goal navigation. Exploration decisions are guided by **Frontier Ranking**, which scores candidate frontiers based on semantic relevance and spatial priors.

The system integrates floor-aware sensing, online map building, and stair-aware obstacle mapping, making it suitable for real-time operation on legged platforms.

## Parameters

| Parameter            | Value   |
|----------------------|---------|
| Framework type       | online  |
| Zero-shot            | true    |
| Floor-aware          | true    |
| LLM integration      | true    |
| Components           | Multi-Floor Abstraction Module, Coarse-to-Fine Reasoning Module |

## Performance

ASCENT was evaluated on two standard multi-floor navigation benchmarks: HM3D and MP3D. It achieves state-of-the-art results in zero-shot multi-floor object-goal navigation, surpassing prior approaches without needing floor-specific retraining or precomputed maps.

## Relationships

- **Uses**: Multi-Floor Abstraction, Coarse-to-Fine Reasoning, LLM ⚠️ ⚠️, Frontier Ranking
- **Depends on**: Zero-Shot Object-Goal Navigation, Multi-floor navigation, Stair-aware Obstacle Mapping, Cross-floor Topology Modeling
- **Evaluated on**: HM3D, MP3D
- **Supersedes**: Prior zero-shot approaches to object-goal navigation in multi-floor environments

## Deployment

ASCENT has been validated on a quadruped robot in real-world multi-floor buildings, demonstrating its ability to navigate stairs, elevators, and open spaces without any environment-specific pre-training. This makes it a practical solution for embodied AI tasks requiring autonomous building-wide exploration.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ASCENT` --extends ⚠️ ⚠️--> `Multi-Floor Abstraction`
- `ASCENT` --extends ⚠️ ⚠️--> `Coarse-to-Fine Reasoning`