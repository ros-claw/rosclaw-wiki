---
id: zero_shot_long_horizon_navigation
title: Zero-shot long-horizon navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:00:35'
last_reinforced: '2026-04-30T04:00:35'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Zero-shot Long-horizon Navigation

**Zero-shot long-horizon navigation** refers to the ability of an embodied agent to navigate over extended distances (long-horizon) in unfamiliar environments without any prior training or access to pre-built 3D maps. This capability is a key enabling technique for autonomous systems operating in unstructured or newly encountered spaces.

## Overview

Traditional navigation pipelines typically require either offline map building, environment-specific training, or both. Zero-shot long-horizon navigation overcomes these constraints by leveraging generalization from a broad distribution of prior data or by combining semantic reasoning with foundation models. It allows the agent to plan and execute a sequence of movements—including turning, traversing corridors, entering rooms, and reaching faraway goals—without ever having seen the specific environment during training.

## Capabilities

- **Navigation without prior training or 3D maps** – The agent can successfully reach a distant goal location in a novel environment using only onboard sensing, without needing a precomputed map or task-specific finetuning.
- **Generalizes to unseen environments** – The approach works across diverse spaces (e.g., different buildings, outdoor areas, or floorplans) thanks to robust visual representation and high-level reasoning.

## Relationships

Zero-shot long-horizon navigation is **used_by** [[TANGO]], a system that integrates this capability to achieve flexible, long-duration autonomy in real-world settings. The concept also draws on principles from [[Zero-shot Learning]] and [[Long-horizon Planning]], and contrasts with traditional [[SLAM]]-based or learned navigation methods that require prior environment exposure.

## Source

This page is based on the findings presented in arxiv paper 2509.08699 (December 2024).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-shot long-horizon navigation` --[[related_to]] ⚠️ ⚠️--> `TANGO` _(wikilink)_
- `Zero-shot long-horizon navigation` --[[related_to]] ⚠️ ⚠️--> `SLAM` _(wikilink)_
