---
id: robo_vln
title: Robo-VLN
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:25:12'
last_reinforced: '2026-04-30T02:25:12'
supersedes: []
sources:
- papers/2104.10674.pdf
source_type: arxiv_paper
---

## Robo-VLN

Robo-VLN is an advanced extension of [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ that lifts the agent off the traditional navigation graph and introduces a more realistic continuous navigation setting. It operates in continuous 3D reconstructed environments, requiring the agent to handle longer trajectories, continuous action spaces, and physical obstacles — closely mirroring real-world navigation challenges.

### Description

Robo-VLN supersedes the discrete VLN navigation graph setting by placing the agent in a fully continuous 3D reconstructed environment. This removes the simplifying assumption of a pre-defined graph and forces the agent to reason directly about spatial geometry and obstacle avoidance. The action space is continuous (e.g., precise steering angles and velocities), and trajectories are significantly longer than in discrete VLN, compounding the difficulty of instruction-following.

### Capabilities

- More closely mimics real-world navigation challenges compared to discrete graph-based VLN.

### Relationships

- **Uses**: [[Continuous 3D reconstructed environments]] ⚠️
- **Depends on**: [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️
- **Supersedes**: [[Discrete VLN navigation graph setting]] ⚠️

### Parameters

- **Environment**: continuous 3D reconstructed
- **Trajectory length**: longer than discrete VLN
- **Action space**: continuous

### Challenges

- Obstacles – the agent must actively avoid physical obstacles in the continuous space, unlike discrete VLN where obstacles are abstracted away by graph edges.