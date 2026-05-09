---
id: locator
title: Locator
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:58:25'
last_reinforced: '2026-04-30T02:58:25'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

# Locator

The **Locator** is a key agent in the [[Where Are You? Dataset]] framework. It is the knowledgeable partner in a two-agent collaborative localization task: while the [[Observer]] moves through an environment with limited global context, the Locator has access to a **detailed [[top-down map]] ⚠️ ⚠️ ⚠️ ⚠️** of the environment and must identify the Observer's location solely through dialogue.

## Overview

The Locator's primary function is to **ask questions** and **give instructions** to the Observer, using the top-down map as ground truth. By leveraging spatial language, the Locator guides the interaction until the Observer's position can be determined with confidence.

## Role

> The Locator has access to a detailed top-down map of the environment and must identify the Observer's location by conversing with the Observer.

This role places the Locator in the position of a "remote expert" — it sees the global layout but cannot observe the Observer directly. All information must pass through natural language exchange.

## Perception

- **Top-down map** — the Locator perceives the world through a static, overhead view of the environment. This map provides room labels, pathways, landmarks, and spatial structure, but does not include real-time sensor data.

## Capabilities

- **Localize Observer on top-down map** — using dialogue to triangulate position relative to map features.
- **Ask questions** — e.g., "Are you near the kitchen counter?" or "Which side of the room are you on?"
- **Give instructions** — e.g., "Walk towards the window," or "Face the blue door."

These capabilities depend on the top-down map and the [[Observer]]'s willingness to respond accurately.

## Relationships

| Relationship | Entity |
|---|---|
| `part_of` | [[Where Are You? Dataset]] |
| `interacts_with` | [[Observer]] |
| `uses` | [[top-down map]] ⚠️ ⚠️ ⚠️ ⚠️ |

- The Locator is a subcomponent of the [[Where Are You? Dataset]] task structure.
- It interacts with the [[Observer]] through a two-way dialogue loop.
- It depends on the [[top-down map]] ⚠️ ⚠️ ⚠️ ⚠️ to generate informed questions and instructions.

## Interaction Protocol

The typical exchange proceeds as follows:

1. The Locator asks a question or issues an instruction based on the map.
2. The [[Observer]] responds with its egocentric view or action feedback.
3. The Locator updates its belief about the Observer's position.
4. The cycle repeats until the Locator is confident enough to declare a location.

This mirrors many **embodied question-answering** and **instruction-following** scenarios studied in [[embodied AI]] and [[VLN]] ⚠️ ⚠️.

## See Also

- [[Where Are You? Dataset]]
- [[Observer]]
- [[top-down map]] ⚠️ ⚠️ ⚠️ ⚠️
- [[embodied AI]]
- [[VLN]] ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Locator` --[[related_to]] ⚠️--> `embodied AI`
