---
id: vision_language_action_vla
title: Vision-Language-Action (VLA)
type: concept
tags: []
confidence: 0.95
created_at: '2026-04-30T00:01:21'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.15258.pdf
- papers/2511.17889.pdf
- papers/2510.03142.pdf
- papers/2412.04453.pdf
source_type: arxiv_paper
---

# Vision-Language-Action (VLA)

A **Vision-Language-Action (VLA)** model is a paradigm in [[Embodied AI]] that integrates visual perception, natural language understanding, and motor action generation into a single end-to-end neural architecture. By processing camera images and textual commands (e.g., "pick up the red cup"), a VLA directly outputs mid-level actions in language form (e.g., "move forward 0.5 meters", "grasp the handle") or high-level action commands for a robotic system, bypassing the need for traditional modular pipelines of object detection, state estimation, and planning. VLA models combine vision, language, and action for embodied tasks.

## General

VLA models leverage pretrained large language models (LLMs) and visual models to learn diverse capabilities from expert data. By transferring rich representations from these foundation models, VLAs acquire a broad understanding of semantics, geometry, and task structure, enabling flexible generalization across environments and instructions. A distinctive characteristic of many modern VLAs is their **output modality**: they generate actions as language tokens (e.g., "move 0.3m left", "rotate 90°") rather than raw joint torques, which allows seamless integration with LLM-based reasoning and simplifies training.

## Definition

Vision-Language-Action (VLA) refers to models that integrate visual input, language instructions, and action outputs into a single neural architecture, enabling robots to execute linguistic commands in the physical world. This unified framework spans perception, reasoning, and control.

## Parameters

- **Domain**: Embodied AI
- **Pipeline**: vision → language reasoning → action
- **Type**: multimodal (processes vision, language, and action modalities)
- **Output**: mid-level actions in language form (e.g., discrete movement primitives or waypoint sequences)
- **Description**: Model combining vision, language, and action for embodied tasks

## Capabilities

- Unified framework for perception, reasoning, and control.
- End-to-end grounding of natural language to physical actions.
- Translates human instructions into executable actions.
- Produces spatial-aware actions (e.g., "move to the left of the table").
- Integrates visual perception, language understanding, and action generation into one model.
- Visual navigation using natural language understanding — interpreting natural language commands to drive a robot through visual environments.

## Subconcepts

- [[spatial grounding]] ⚠️ – Mapping language references (e.g., "to the left of the box") into spatial coordinates.
- [[scene reasoning]] ⚠️ – Understanding object relationships, affordances, and task context from visual scenes.
- [[long-horizon navigation]] ⚠️ – Generating sequences of actions that span long distances or multiple tasks using language guidance.

## Related Concepts

- [[Embodied AI]] – VLA is a core architectural approach within embodied intelligence.
- [[Visual Language Navigation]] ⚠️ – VLA models can be directly applied to navigation tasks that combine vision and language instructions.

## Usage

VLA is a foundational concept used in the [[VLA-AN]] architecture, where it forms the core perception-to-action loop.

### Used By

- [[MM-Nav]] – Multimodal navigation system that applies VLA models to integrate vision and language for path planning in dynamic environments.
- [[NaVILA]] – A navigation system that leverages a VLA model to output mid-level, language-form actions for zero-shot visual navigation.

---

### Sources

- [[data/raw/papers/2412.04453.pdf]] ⚠️ — arxiv preprint 2412.04453.
- [[data/raw/papers/2512.15258.pdf]] ⚠️ — arxiv preprint 2512.15258.
- [[data/raw/papers/2511.17889.pdf]] ⚠️ — arxiv preprint 2511.17889.
- [[data/raw/papers/2510.03142.pdf]] ⚠️ — arxiv preprint 2510.03142.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Vision-Language-Action (VLA)` --[[related_to]] ⚠️ ⚠️ ⚠️--> `VLA-AN` _(wikilink)_
- `Vision-Language-Action (VLA)` --[[related_to]] ⚠️ ⚠️ ⚠️--> `Embodied AI` _(wikilink)_
- `Vision-Language-Action (VLA)` --[[related_to]] ⚠️ ⚠️ ⚠️--> `Visual Language Navigation` _(wikilink)_
- `Vision-Language-Action (VLA)` --[[used_by]] ⚠️ ⚠️--> `MM-Nav` _(wikilink)_
- `Vision-Language-Action (VLA)` --[[used_by]] ⚠️ ⚠️--> `NaVILA` _(wikilink)_