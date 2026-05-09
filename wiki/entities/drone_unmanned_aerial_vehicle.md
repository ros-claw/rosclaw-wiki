---
id: drone_unmanned_aerial_vehicle
title: Drone (Unmanned Aerial Vehicle)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:08:20'
last_reinforced: '2026-04-29T21:08:20'
supersedes: []
sources:
- papers/2205.12219.pdf
source_type: arxiv_paper
---

## Drone (Unmanned Aerial Vehicle)

A **Drone**, or Unmanned Aerial Vehicle (UAV), is an aircraft operated without a human pilot onboard. In the context of embodied AI and human-robot interaction, drones are increasingly equipped with natural language interfaces and autonomous decision-making capabilities. This page describes a drone system capable of high-level human-robot collaboration through conversational commands.

### Capabilities

- **Navigate via natural language conversation**: The drone can interpret spoken or typed instructions to plan and execute flight paths, making it accessible to non-expert users.
- **Follow commander instructions and ask questions when needed**: When instructions are ambiguous or unsafe, the drone proactively queries the human for clarification, improving mission reliability.
- **Relieve human controller burden, enable multitasking, improve accessibility for disabilities**: By offloading low-level piloting and interpretation tasks, the drone allows operators to focus on other activities and supports users with limited mobility or visual impairments.

### Relationships

- **Uses** [[Natural Language Processing]] ⚠️ to understand and generate conversational responses.
- **Uses** [[Computer Vision]] ⚠️ for environment perception, obstacle avoidance, and target recognition.
- **Uses** [[Human Attention]] ⚠️ modeling to infer user focus and coordinate shared attention during tasks.

These capabilities are sourced from the paper *Language-Guided Human-Robot Collaboration on a Drone* (arXiv:2205.12219). The drone’s architecture integrates large language models and vision transformers to enable real-time, grounded dialogue between the operator and the aerial platform.