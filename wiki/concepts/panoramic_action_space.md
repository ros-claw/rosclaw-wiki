---
id: panoramic_action_space
title: Panoramic Action Space
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:57:05'
last_reinforced: '2026-04-30T02:57:05'
supersedes: []
sources:
- papers/1806.02724.pdf
source_type: arxiv_paper
---

## Overview

A **Panoramic Action Space** defines the set of actions available to an agent during [[Vision-and-Language Navigation]]. Rather than using low-level motor commands, this action space is designed to match the **granularity of human-generated instructions**, focusing on high-level decisions and navigation landmarks. It is a central component of the [[Speaker-Follower Model]] for instruction following.

## Parameters

- **Granularity**: The action space reflects the level of detail found in natural language instructions, avoiding micro‑actions that are rarely mentioned.
- **Action Types**: The space consists of high-level decisions (e.g., turn, go forward, stop) and references to **landmarks** (salient features in the environment) that align with human route descriptions.

## Capabilities

- **Supports pragmatic reasoning**: By operating at a semantic level, the action space enables the agent to reason about the intent behind instructions rather than raw motor commands.
- **Enables efficient instruction following**: The high-level actions reduce the search space and simplify the mapping from language to behavior, improving both data augmentation and real‑world navigation.

## Relationships

- **used_by** [`[[Speaker-Follower Model]]` – The panoramic action space is explicitly employed by the Speaker‑Follower architecture to generate and evaluate navigation trajectories.
- **depends_on** [`[[Landmark Detection]] ⚠️` – Identifying landmarks in panoramic views is necessary to populate the action space.
- **implements** [`[[Pragmatic Reasoning]]` – The action space serves as the interface through which the agent performs pragmatic reasoning during instruction following.

## Usage in the Speaker‑Follower Model

In the [[Speaker-Follower Model]], the panoramic action space is used for two primary roles:

1. **Data augmentation**: The model samples actions from the panoramic set to generate synthetic trajectories, which are then paraphrased by the speaker module into new instructions.
2. **Pragmatic reasoning**: During inference, the follower evaluates actions in the panoramic space to decide which move best satisfies the instruction, incorporating contextual cues and landmark references.

This design ensures that the agent’s decisions remain interpretable and tightly coupled to typical human navigation language.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Panoramic Action Space` --[[related_to]] ⚠️ ⚠️--> `Vision-and-Language Navigation`
**Pending review:**
- `Panoramic Action Space` --[[related_to]] ⚠️ ⚠️--> `Speaker-Follower Model` _(wikilink)_
