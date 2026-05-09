---
id: mid_level_language_action_generation
title: Mid-level Language Action Generation
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T00:45:42'
last_reinforced: '2026-04-30T00:45:42'
supersedes: []
sources:
- papers/2412.04453.pdf
source_type: arxiv_paper
---

**Mid-level Language Action Generation** is a skill that translates high-level natural language instructions into mid-level action primitives, providing an interpretable intermediate representation between abstract commands and low-level joint or motor commands. It is a core component of the [[NaVILA framework]] ⚠️ ⚠️ for embodied navigation.

### Overview

Mid-level actions serve as a bridge between human‑readable commands (e.g., "go to the kitchen") and the precise control signals required by a robot’s actuators. Instead of directly outputting motor torques or joint angles, this skill generates structured, semantically meaningful actions such as `"moving forward 75cm"`. These actions often incorporate spatial information (e.g., distance, angle) to make the intermediate representation interpretable and reusable across different hardware platforms.

### Parameters

| Parameter   | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| format      | A structured string pattern, e.g., `"moving forward 75cm"` or `"turn left 90°"` |
| spatial_info| Boolean flag indicating whether the action includes explicit spatial quantities (distance, orientation, etc.) – typically `true` |

### Capabilities

- **Bridges high-level instructions and low-level control** – Converts abstract goals (e.g., “navigate to the table”) into discrete, executable steps that can be mapped to low-level policies.
- **Provides an interpretable intermediate representation** – The generated actions are human‑readable, facilitating debugging, user feedback, and policy introspection.

### Usage

This skill is **used_in** the [[NaVILA framework]] ⚠️ ⚠️, where it acts as the output of the language‑to‑action module. The mid‑level actions are then consumed by a low‑level controller or a motion planner to produce joint‑space commands. By decoupling high‑level reasoning from low‑level actuation, the system gains flexibility and modularity.

### Related Concepts

- [[High-Level Instructions]] ⚠️ – the input to this skill.
- [[Low-Level Control]] ⚠️ – the target representation that mid‑level actions are translated into.
- [[Embodied Navigation]] – the broader task domain where mid‑level actions are applied.
- [[Sim-to-Real Transfer]] – benefits from the interpretable nature of mid‑level actions during domain adaptation.