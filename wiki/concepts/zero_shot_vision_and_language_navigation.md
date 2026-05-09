---
id: zero_shot_vision_and_language_navigation
title: Zero-Shot Vision-and-Language Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:36:16'
last_reinforced: '2026-04-29T20:36:16'
supersedes: []
sources:
- papers/2601.06806.pdf
source_type: arxiv_paper
---

# Zero-Shot Vision-and-Language Navigation

## Overview

**Zero-Shot Vision-and-Language Navigation (Zero-Shot VLN)** is a variant of [[Vision-and-Language Navigation]] where agents must follow natural language instructions without any prior training on navigation tasks. Instead of relying on task-specific supervised learning, these agents leverage **pre-exploration** of the environment and **generalizable spatial representations**—such as Spatial Scene Graphs (SSGs)—to plan and execute actions. This approach enables navigation in novel environments without requiring fine‑tuning.

## Key Parameters

- **Setting**: Agents are allowed to fully explore the environment before task execution, building a mental or explicit map of the space.
- **Core challenge**: The lack of implicit spatial knowledge that would normally be extracted from training data (e.g., typical floorplans, object layouts).
- **Solution**: Use explicit global spatial representations, such as **Spatial Scene Graphs** ([[Spatial Scene Graph]]), to encode the geometry and topology of the environment in a way that is interpretable and actionable from language instructions.

## Capabilities

- **Navigate based on natural language instructions** without task‑specific training data.
- **Generalize across environments** without any fine‑tuning, because the policy is grounded in an explicit structural representation rather than memorized patterns.

## Related Concepts

- **Subtype of**: [[Vision-and-Language Navigation]] — Zero-Shot VLN inherits the core problem of grounding language to action but removes the need for in‑domain training.
- **Related to**: [[Zero-Shot Learning]] — The ability to perform a task (VLN) without having seen any examples of that task during training.
- **Depends on**: [[Spatial Scene Graph]] — The primary representation used to bridge language and physical space.
- **Contrasts with**: standard VLN models that rely on large datasets of instruction‑trajectory pairs.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-Shot Vision-and-Language Navigation` --[[related_to]] ⚠️--> `Spatial Scene Graph`
