---
id: vision_and_language_navigation_vln_for_legged_robots
title: Vision-and-Language Navigation (VLN) for legged robots
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:45:03'
last_reinforced: '2026-04-30T00:45:03'
supersedes: []
sources:
- papers/2412.04453.pdf
source_type: arxiv_paper
---

# Vision-and-Language Navigation (VLN) for Legged Robots

**Vision-and-Language Navigation (VLN)** for legged robots is a [[concept]] ⚠️ that enables robots to navigate complex, cluttered environments by interpreting natural language commands alongside visual input. It combines [[vision]] ⚠️ ⚠️ (usually from an onboard camera) and [[natural language]] ⚠️ ⚠️ instructions to produce navigation actions, making human–robot interaction more intuitive.

## Domain and Modality

- **Domain**: [[legged robotics]] ⚠️
- **Modality**: [[vision]] ⚠️ ⚠️ and [[language]] ⚠️

## Capabilities

- Allows humans to command a robot using [[natural language]] ⚠️ ⚠️ (e.g., "walk to the red chair and step over the cable").
- Enables navigation in [[cluttered scenes]] ⚠️ where traditional planners may fail (e.g., stairs, debris, narrow passages).

## Implementation

VLN for legged robots is implemented by the system **[[NaVILA]]**, which directly integrates vision-language models with whole-body locomotion control.

## Relationship Map

- [[NaVILA]] *implements* Vision-and-Language Navigation (VLN) for legged robots.
- VLN *depends on* [[Visual Perception]] ⚠️, [[Language Understanding]] ⚠️, and [[Motion Planning]] ⚠️.
- VLN is a *variant of* [[Vision-and-Language Navigation (general)]] ⚠️ adapted for [[Legged Robots]].

## Related Pages

- [[NaVILA]]
- [[Legged Locomotion]] ⚠️
- [[Language-Guided Robotics]] ⚠️
- [[Human-Robot Interaction]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Vision-and-Language Navigation (VLN) for legged robots` --[[applies_to]] ⚠️--> `Legged Robots`
**Pending review:**
- `Vision-and-Language Navigation (VLN) for legged robots` --[[related_to]] ⚠️--> `NaVILA` _(wikilink)_
