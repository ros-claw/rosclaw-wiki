---
id: vision_driven_embodied_agent_pipeline
title: Vision-driven Embodied Agent Pipeline
type: algorithm
tags: []
confidence: 0.6
created_at: '2026-04-29T21:55:27'
last_reinforced: '2026-04-29T21:55:27'
supersedes: []
sources:
- articles/article.md
source_type: blog_post
---

# Vision-driven Embodied Agent Pipeline

**Type:** Algorithm  

A unified framework for processing multimodal inputs, reasoning through interactions, and generating structured executable plans composed of sequential actions. The Vision-driven Embodied Agent Pipeline is designed to bridge perception and action by leveraging Multi-modal Large Language Models (MLLMs) ⚠️ ⚠️ as core reasoning engines. It is used by EmbodiedBench to evaluate the capability of MLLMs as embodied agents.

## Pipeline Overview

The pipeline operates in four sequential stages:

1. **Visual State Description** — extracts a textual or structured representation of the current visual observation from the environment.
2. **Reflection and Reasoning** — analyzes the state description, considering task goals, prior knowledge, and potential outcomes.
3. **Language Plan Generation** — produces a high-level plan expressed in natural language (e.g., "pick up the red cube").
4. **Executable Plan Generation** — converts the language plan into a sequence of low-level actions or API calls that can be directly executed by the robot.

## Capabilities

- **Multimodal Input Processing** — accepts visual (image/video), language (instruction), and optionally other sensor streams.
- **Structured Plan Generation** — produces plans that are both human‑readable and directly executable by downstream control systems.

## Relationships

- **used_by** → EmbodiedBench (the pipeline serves as the agent evaluation framework)
- **uses** → Multi-modal Large Language Models (MLLMs) ⚠️ ⚠️ (the reasoning and plan generation stages depend on MLLM capabilities)

## Additional Context

This pipeline is a key component of the EmbodiedBench benchmark, which tests how well MLLMs can function as embodied agents in simulated and real‑world tasks. The structured nature of the output allows for direct comparison across different model architectures and training regimes.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Vision-driven Embodied Agent Pipeline` --implements ⚠️--> `EmbodiedBench`
