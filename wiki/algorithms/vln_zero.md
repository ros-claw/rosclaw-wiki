---
id: vln_zero
title: VLN-Zero
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:29:11'
last_reinforced: '2026-04-30T00:29:11'
supersedes: []
sources:
- papers/2509.18592.pdf
source_type: arxiv_paper
---

# VLN-Zero

**VLN-Zero** is a two-phase vision-language navigation framework that combines rapid exploration with symbolic reasoning and cache-enabled execution for zero-shot transfer in robot navigation. It enables robots to navigate unfamiliar environments without prior training or fine-tuning, leveraging [[Vision-Language Models (VLM)]] ⚠️ ⚠️ ⚠️ and [[Scene Graphs]] to achieve robust decision-making.

## Overview

The framework operates in two distinct phases: **exploration** and **deployment**. During exploration, the robot rapidly maps the environment and constructs compact symbolic scene graphs. In the deployment phase, a neurosymbolic planner uses these graphs and cached task-location trajectories to navigate efficiently, with minimal reliance on expensive VLM calls.

## Phases

- **Exploration Phase**: The agent builds a [[Scene Graph]] ⚠️ of the environment using structured prompts and [[Vision-Language Models (VLM)]] ⚠️ ⚠️ ⚠️ to recognize objects, regions, and spatial relationships.
- **Deployment Phase**: A [[Neurosymbolic Planning]] module reasons over the scene graph to generate navigation plans, reusing cached trajectories from prior tasks via **Cache-Enabled Execution**.

## Capabilities

- Rapid exploration of unseen environments
- Efficient construction of compact symbolic scene graphs
- Zero-shot neurosymbolic navigation
- Cache-enabled execution for reusing task-location trajectories
- Robust decision-making in unseen environments

## Performance

VLN-Zero achieves **2x higher success rate** than state-of-the-art zero-shot models and outperforms most fine-tuned baselines. It reaches goal locations in **half the time** and uses **55% fewer VLM calls** on average, demonstrating both speed and computational efficiency.

## Relationships

- **Uses**: [[Vision-Language Models (VLM)]] ⚠️ ⚠️ ⚠️, [[Scene Graphs]], [[Neurosymbolic Planning]], [[Cache-Enabled Execution]]
- **Depends On**: structured prompts, scene graph construction
- **Implements**: zero-shot visual language navigation

## Source

- ArXiv paper: `papers/2509.18592.pdf` — "VLN-Zero: A Two-Phase Zero-Shot Vision-Language Navigation Framework"