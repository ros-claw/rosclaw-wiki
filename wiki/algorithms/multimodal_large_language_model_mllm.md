---
id: multimodal_large_language_model_mllm
title: Multimodal Large Language Model (MLLM)
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:55:47'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.20499.pdf
- papers/2511.06840.pdf
- papers/2502.09560.pdf
source_type: arxiv_paper
---

### Multimodal Large Language Model (MLLM)

A **Multimodal Large Language Model (MLLM)** is a neural network model that extends the capabilities of Large Language Models to process and reason over multiple modalities — typically **text** and **image**, and possibly other modalities. As high‑capacity reasoning cores, MLLMs integrate natural language understanding with visual perception to generate executable actions for embodied agents.

#### Parameters
- **Type**: neural network model
- **Modalities**: text, image, possibly other modalities (e.g., depth maps, audio)

#### Capabilities
- **High‑level semantic understanding** – interprets natural language instructions and visual scene semantics.
- **Low‑level atomic action planning** – translates reasoning into concrete actions (e.g., "move forward 0.5 m", "turn left 30°").
- **Commonsense reasoning** – leverages prior knowledge to infer plausible outcomes and navigate novel situations.
- **Complex instruction understanding** – comprehends multi‑step, context‑dependent commands.
- **Spatial awareness** – infers object locations, distances, and obstacles from visual input.
- **Visual perception** – processes camera images, depth maps, and topological representations.
- **Long‑term planning** – reasons over exploration history and future steps using structured prompts (e.g., TopoGraph-and-VisitInfo-Aware Prompting).

#### Relationships
- **Uses**: TopoGraph-and-VisitInfo-Aware Prompting  
  The MLLM leverages topological graph‑based prompts that encode the spatial environment and visitation history to inform decision‑making.
- **Depends on**: Abstract Obstacle Map‑Based Waypoint Predictor ⚠️ ⚠️  
  For precise, obstacle‑aware waypoint generation, the MLLM relies on this predictor.
- **Used in**: Zero‑Shot VLN ⚠️ ⚠️  
  Acts as the core reasoning engine for zero‑shot visual‑language navigation.
- **Used in**: PanoNav  
  Provides perception and reasoning without explicit mapping.
- **Used in**: Vision‑Driven Embodied Agents ⚠️ ⚠️  
  MLLMs serve as the reasoning backbone for a wide class of embodied agents that rely on visual observation.
- **Evaluated by**: EmbodiedBench  
  A benchmark that tests 24 leading proprietary and open‑source MLLMs, revealing performance gaps between high‑level and low‑level tasks.

#### Role
The MLLM provides perception and reasoning for navigation tasks without requiring an explicit map. By jointly processing language instructions and visual inputs, it can generate goal‑directed behavior directly from sensory data, enabling open‑loop and zero‑shot deployment.

#### Role in Zero‑Shot VLN
The MLLM is used as the reasoning core of the zero‑shot framework, processing topographical and visitation information to make navigation decisions. It receives as input a natural language instruction, a current visual observation, and a topological graph of the environment along with past visitation data. Using this context, it generates a sequence of low‑level actions that fulfill the instruction without requiring any fine‑tuning on navigation data.

#### Role in Embodied AI
MLLMs serve as the reasoning backbone for vision‑driven embodied agents. EmbodiedBench systematically evaluates 24 leading proprietary and open‑source MLLMs, revealing a consistent performance gap between high‑level semantic understanding and low‑level atomic action planning. This finding motivates further research into bridging the two levels within a unified MLLM framework.

#### Further Reading
- Zero‑Shot VLN ⚠️ ⚠️
- Large Language Model
- Abstract Obstacle Map‑Based Waypoint Predictor ⚠️ ⚠️
- PanoNav
- EmbodiedBench
- Vision‑Driven Embodied Agents ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Multimodal Large Language Model (MLLM)` —extends ⚠️ ⚠️--> `TopoGraph-and-VisitInfo-Aware Prompting`
- `Multimodal Large Language Model (MLLM)` —extends ⚠️ ⚠️--> `Abstract Obstacle Map-Based Waypoint Predictor`