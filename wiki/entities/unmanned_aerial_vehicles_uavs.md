---
id: unmanned_aerial_vehicles_uavs
title: Unmanned Aerial Vehicles (UAVs)
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:28:18'
last_reinforced: '2026-04-30T00:28:18'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

# Unmanned Aerial Vehicles (UAVs)

**Unmanned Aerial Vehicles (UAVs)** — commonly known as drones — are autonomous or remotely piloted aircraft that operate without a human pilot onboard. In robotics, UAVs represent a critical class of **aerial robots** used for tasks ranging from surveying and delivery to search-and-rescue and environmental monitoring.

## Overview

UAVs combine airframe, propulsion, avionics, and onboard computing to perform autonomous flight. They are increasingly integrated with advanced perception and planning systems, enabling complex missions such as Vision-Language Navigation (VLN) in outdoor environments.

## Capabilities (entity: capability)

- **Language-guided flight**: UAVs can interpret natural language instructions to plan and execute flight paths, enabled by Vision-Language Models ⚠️ ⚠️ ⚠️ (VLMs).
- **Long-horizon trajectory planning**: UAVs are capable of reasoning over extended time horizons to generate collision-free, goal-directed trajectories through complex 3D space.

## Navigation Challenges

UAVs operating in outdoor aerial environments face several unique obstacles:

- **Vast complexity of scenes**: Outdoor environments contain varied terrain, dynamic objects, changing lighting, and occlusions that challenge visual perception.
- **Data acquisition difficulties**: Collecting high-quality, labeled training data for aerial VLN is expensive and logistically demanding, due to the need for multiple viewpoints and diverse conditions.
- **Long-horizon planning requirements**: Successful navigation often requires reasoning over long sequences of actions with delayed feedback, demanding robust planning algorithms.

The **OpenVLN framework ⚠️ ⚠️** directly addresses these challenges by fine-tuning Vision-Language Models ⚠️ ⚠️ ⚠️ with rule-based policies and a dedicated long-horizon planner tailored for UAV flight.

## Relationships

- **`uses`**: Vision-Language Models ⚠️ ⚠️ ⚠️ — VLMs provide the visual-language grounding that enables language-guided flight.
- **`uses`**: OpenVLN framework ⚠️ ⚠️ — This framework delivers end-to-end VLN capabilities specifically adapted for UAVs.
- **`depends_on`**: Rule-based policies — Used during fine-tuning to inject structured prior knowledge into the VLM.
- **`depends_on`**: Long-horizon planner ⚠️ — Generates feasible, long-term trajectories respecting vehicle dynamics and environmental constraints.

## Applications

UAVs equipped with vision-language capabilities can be deployed in:

- Aerial search-and-rescue
- Infrastructure inspection
- Precision agriculture
- Environmental monitoring
- Package delivery in complex terrains