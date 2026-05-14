---
id: zero_shot_vln_framework_with_topograph_prompting
title: Zero-Shot VLN Framework with TopoGraph Prompting
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:42:08'
last_reinforced: '2026-04-30T00:42:08'
supersedes: []
sources:
- papers/2509.20499.pdf
source_type: arxiv_paper
---

# Zero-Shot VLN Framework with TopoGraph Prompting

## Overview

The **Zero-Shot VLN Framework with TopoGraph Prompting** is a state-of-the-art approach for vision-language navigation (VLN) that operates entirely without environment-specific training. It combines a geometric waypoint predictor with a multimodal large language model (MLLM) guided by a topological graph and visitation history. The framework achieves strong performance on standard benchmarks while requiring zero task-specific fine-tuning.

## Architecture

The framework comprises two core components:

- **Abstract Obstacle Map-Based Waypoint Predictor** – A lightweight module that converts sensor observations into an abstract obstacle map and outputs linearly reachable candidate waypoints. This provides a geometric basis for local navigation.

- **TopoGraph-and-VisitInfo-Aware Prompting** – A prompting mechanism that dynamically constructs a topological graph from visited and candidate waypoints, annotated with visitation records. This graph, along with relevant visit information, is encoded into prompts for the MLLM.

These components are fed into a **Multimodal Large Language Model (MLLM)**, which reasons over both visual and textual information to select the next waypoint and generate low-level control commands (e.g., heading changes, forward motion). The agent thus performs local path planning and error correction within a continuous environment.

## Performance

- **Dataset**: R2R-CE (continuous evaluation of Room-to-Room)
  - **Success rate**: 41%
- **Dataset**: RxR-CE (continuous evaluation of Room-x-Room)
  - **Success rate**: 36%
- This system achieves **state-of-the-art results among zero-shot methods** on both benchmarks, demonstrating that zero-shot VLN in continuous spaces is feasible without any training on the target environments.

## Key Capabilities

- Navigates in **continuous environments** without task-specific training.
- Combines **geometric reasoning** (obstacle map, waypoint reachability) with **semantic reasoning** (MLLM's understanding of instructions and context).
- Performs **local path planning and error correction** through iterative waypoint selection and action generation.

## Relationships

- **Implements**: Vision-Language Navigation (VLN)
- **Comprises**: Abstract Obstacle Map-Based Waypoint Predictor, TopoGraph-and-VisitInfo-Aware Prompting
- **Uses**: Multimodal Large Language Model (MLLM)
- **Depends on**: Topological graph construction, abstract obstacle map generation
- **Applies to**: R2R-CE, RxR-CE benchmarks, any continuous VLN task requiring zero-shot generalization.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-Shot VLN Framework with TopoGraph Prompting` --applies_to ⚠️ ⚠️--> `R2R-CE`
- `Zero-Shot VLN Framework with TopoGraph Prompting` --applies_to ⚠️ ⚠️--> `RxR-CE`
**Pending review:**
- `Zero-Shot VLN Framework with TopoGraph Prompting` --related_to ⚠️ ⚠️ ⚠️--> `Abstract Obstacle Map-Based Waypoint Predictor` _(wikilink)_
- `Zero-Shot VLN Framework with TopoGraph Prompting` --related_to ⚠️ ⚠️ ⚠️--> `TopoGraph-and-VisitInfo-Aware Prompting` _(wikilink)_
- `Zero-Shot VLN Framework with TopoGraph Prompting` --related_to ⚠️ ⚠️ ⚠️--> `Multimodal Large Language Model (MLLM)` _(wikilink)_
