---
id: object_goal_navigation
title: Object Goal Navigation
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T04:30:34'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2312.03275.pdf
- code/PKU-SEC-Lab_EfficientNav/README.md
source_type: arxiv_paper
---

Object Goal Navigation (ObjectNav or ObjNav) is a common and fundamental embodied AI task in which an agent (or robot) must locate and navigate to a specific instance of a given target object category (e.g., "find a chair") within an unseen environment, relying only on on‑board sensors and no prior map.

## Capabilities

- Navigate to an instance of a given target object category in a previously unknown environment.  
- Recognise and localise objects of the specified category using visual perception.  
- Plan a collision‑free path toward the identified object.  

## Evaluation

Object Goal Navigation is typically evaluated using **SPL (Success weighted by Path Length) ⚠️**, which measures both success in reaching the goal and the efficiency of the path taken.

## Related Concepts

- **VLFM (Value‑Driven Latent Flow Model) ⚠️** – an approach that frames Object Goal Navigation as a problem of learning a latent flow field, using reward‑driven navigation to improve performance and generalisation.
- **Embodied AI** – Object Goal Navigation is a core task within this broader field.
- **EfficientNav** – a system that addresses the Object Goal Navigation task, focusing on efficient exploration and goal‑directed navigation.