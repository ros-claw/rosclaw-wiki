---
id: boston_dynamics_spot
title: Boston Dynamics Spot
type: entity
tags: []
confidence: 0.9
created_at: '2026-04-29T21:39:11'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2312.03275.pdf
- papers/2411.07848.pdf
source_type: arxiv_paper
---

# Boston Dynamics Spot

**Boston Dynamics Spot** is a quadrupedal mobile manipulation robot designed for a variety of real-world tasks, including navigation and object interaction in complex indoor environments. As a **quadruped robot**, it serves as a versatile test platform for real‑world evaluation of embodied AI systems, notably for real‑world validation of the [[VLFM]] framework.

## Overview

Spot is a commercially available platform known for its agility, payload capacity, and ability to traverse unstructured terrain. It is commonly used in research and industry for inspection, mapping, data collection, and mobile manipulation tasks. In the context of embodied AI, Spot acts as a mobile base for vision‑language models and manipulation systems, and its ability to carry a manipulator arm makes it well suited for field deployments. The platform is equipped with an **RGB‑D camera**, enabling depth‑aware perception for semantic navigation and object interaction.

## Capabilities

- **Mobile manipulation** – Can carry a manipulator arm and interact with objects during navigation.
- **Navigation in office buildings** – Demonstrated ability to localize itself and move through hallways, doorways, and rooms without prior map knowledge when equipped with appropriate control policies.
- **Zero‑shot object‑centric instruction following** – Using the Language‑Inferred Factor Graph for Instruction Following ([[LIFGIF]] ⚠️ ⚠️) system, Spot can follow natural language commands to locate and interact with objects without requiring task‑specific fine‑tuning.
- **RGB‑D perception** – The on‑board RGB‑D camera provides both visual and depth data, enabling dense semantic mapping and obstacle avoidance in unstructured environments.
- **Deployment with VLFM** – Spot serves as the primary test platform for the [[VLFM]] (Vision‑Language Foundation Model) system, used for object‑driven navigation and semantic querying of its environment.

## Relationships

Spot:
- uses the [[VLFM]] system for object‑driven navigation and semantic querying of its environment.
- uses the [[Language‑Inferred Factor Graph for Instruction Following (LIFGIF)]] ⚠️ system for zero‑shot instruction following in real‑world settings.
- is equipped with an [[RGB‑D camera]] ⚠️ for depth‑aware perception.

## Real‑world Deployment

In a study documented in *arXiv:2312.03275*, Spot was deployed with the [[VLFM]] framework to search for and navigate to target objects in an unfamiliar office building. The robot successfully located objects such as a coffee mug and a chair without prior knowledge of the building layout, leveraging natural language instructions and visual perception (RGB‑D camera data). This demonstration validates the platform’s suitability for deploying model‑based autonomy in real‑world, unstructured spaces.

More recently, Spot has been used as a test platform for the [[LIFGIF]] ⚠️ ⚠️ system, which infers factor graphs from language to guide navigation and manipulation. These deployments further highlight Spot’s role as a robust, off‑the‑shelf platform for evaluating novel algorithms in realistic environments.