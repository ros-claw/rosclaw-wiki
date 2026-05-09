---
id: lovon
title: LOVON
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:54:01'
last_reinforced: '2026-04-30T03:54:01'
supersedes: []
sources:
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# LOVON

**LOVON** (Long-range Open-Vocabulary Object Navigation) is an algorithm designed for autonomous long-range object navigation in dynamic, unstructured environments. It integrates [[Large Language Models (LLMs)]] for hierarchical task planning and [[Open-Vocabulary Visual Detection]] ⚠️ ⚠️ ⚠️ models to identify and track arbitrary targets in real time. LOVON is built for plug-and-play deployment across [[Legged Robots]] and other mobile platforms.

## Capabilities

- **Autonomous navigation** over long distances in complex, changing environments.
- **Task adaptation** via LLM-driven high-level planning.
- **Robust task completion** despite dynamic obstacles and temporary target occlusions.
- **Real-time detection, search, and navigation** toward open-vocabulary dynamic targets.
- **Plug-and-play compatibility** – LOVON can be dropped into different legged robot platforms without extensive retuning.

## Key Components

### LLM Integration – Hierarchical Task Planning
LOVON leverages [[Large Language Models (LLMs)]] to decompose long-range navigation missions into a hierarchy of sub-tasks. The LLM provides high-level reasoning (e.g., "go to the kitchen, then find the cup"), while lower-level controllers handle locomotion and real-time obstacle avoidance.

### Open-Vocabulary Visual Detection
The algorithm uses [[Open-Vocabulary Visual Detection]] ⚠️ ⚠️ ⚠️ models to identify target objects without prior training on specific categories. This enables searching for and navigating toward arbitrary objects (e.g., "a red ball", "the nearest chair") in novel environments.

### Hierarchical Task Planning
LOVON implements **Hierarchical Task Planning** – a structured approach that separates high-level mission planning from low-level execution. Each sub-task (e.g., "go to room A", "find object X") is executed in sequence, with status feedback loops to the LLM.

### Open-Vocabulary Object Navigation
By combining visual detection with hierarchical planning, LOVON achieves **Open-Vocabulary Object Navigation**: the ability to locate and approach any object described in natural language, even if the robot has never seen it before.

## Visual Stabilization

Real-world deployments on legged robots suffer from **visual jittering** due to gait and terrain. LOVON employs **[[Laplacian Variance Filtering]]** (a dependency) to stabilize camera feed, ensuring consistent detection and tracking performance during motion.

## Dealing with Blind Zones and Temporary Target Loss

LOVON incorporates dedicated strategies for handling blind zones and temporary loss of target visibility. While the exact mechanisms are not detailed in the source abstract, the system is designed to:
- Recover from occlusions by re-planning search paths.
- Maintain belief about target location using prior detections and environment context.

## Relationship Annotations

- **Uses**: [[Large Language Models (LLMs)]], [[Open-Vocabulary Visual Detection]] ⚠️ ⚠️ ⚠️
- **Depends on**: [[Laplacian Variance Filtering]]
- **Implements**: [[Hierarchical Task Planning]], [[Open-Vocabulary Object Navigation]] ⚠️
- **Part of**: (none)

## Source

Based on arXiv paper **2507.06747** – "LOVON: Long-range Open-Vocabulary Object Navigation for Legged Robots in Dynamic Environments."

## See Also

- [[Autonomous Navigation]] ⚠️
- [[Legged Robots]]
- [[Dynamic Unstructured Environments]] ⚠️
- [[Sim-to-Real Transfer]] (potential application area)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `LOVON` --[[implements]] ⚠️ ⚠️--> `Large Language Models (LLMs)`
- `LOVON` --[[implements]] ⚠️ ⚠️--> `Legged Robots`
