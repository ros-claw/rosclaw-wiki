---
id: objectnav
title: ObjectNav
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:56:41'
last_reinforced: '2026-04-29T23:56:41'
supersedes: []
sources:
- papers/2509.16445.pdf
source_type: arxiv_paper
---

# ObjectNav

**Object Navigation (ObjectNav)** is a task in embodied AI where a robot or agent must navigate through an environment to locate and reach an instance of a target object category. The agent is given only the category label (e.g., "chair") and must explore the space, recognize the object, and plan a path to it. ObjectNav is a core benchmark for evaluating spatial reasoning, exploration, and semantic understanding in navigation agents.

## Parameters

- **Task type**: object goal navigation
- **Benchmark**: HM3D ObjectNav ⚠️ (part of the Habitat-Matterport 3D dataset)
- **Metrics**: 
  - SPL (Success weighted by Path Length)
  - success rate ⚠️

## Capabilities

- Serves as a training task for navigation agents
- Requires the agent to find specific object categories in unseen environments

## Relationships

- `part_of`: FiLM-Nav training mixture — ObjectNav is one of the diverse task types used to train FiLM-Nav, a multi-task navigation model.
- `used_in`: HM3D benchmark ⚠️ — ObjectNav is a standard evaluation in the HM3D benchmark suite.

## Description

ObjectNav is a fundamental task in embodied AI. The agent starts at a random location in a previously unseen 3D environment and must navigate to an object from a known category (e.g., "toilet", "bed", "couch"). Success is defined by reaching within a threshold distance of the target. FiLM-Nav incorporates ObjectNav as part of its diverse training data, enabling policy generalization across different navigation objectives. The task challenges visual perception, exploration strategies, and goal-oriented path planning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `ObjectNav` --related_to ⚠️--> `FiLM-Nav` _(wikilink)_
