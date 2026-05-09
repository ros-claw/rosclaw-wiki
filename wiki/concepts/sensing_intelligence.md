---
id: sensing_intelligence
title: Sensing Intelligence
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:47:25'
last_reinforced: '2026-04-30T03:47:25'
supersedes: []
sources:
- papers/2508.15354.pdf
source_type: arxiv_paper
---

# Sensing Intelligence

**Sensing Intelligence** is a concept in [[Embodied Navigation]] that refers to the capability of an autonomous agent to interpret raw sensor data into actionable information for spatial reasoning and movement. It forms the perceptual backbone that enables an embodied system to understand and navigate its environment.

## Role in Embodied Navigation

Sensing Intelligence is a fundamental component of [[Embodied Navigation]], supplying the real-time, context-aware understanding of the environment needed for path planning, obstacle avoidance, and goal-reaching. It bridges low-level sensor streams (e.g., from cameras, LiDAR, IMU) with higher-level planning and control loops.

## Relationship

- **part_of** → [[Embodied Navigation]] – sensing intelligence is one of the core capabilities that constitutes embodied navigation.

## Key Functions

- **Environmental perception**: extracting features such as geometry, semantic labels, and dynamic object positions.
- **Self-state estimation**: using proprioceptive and exteroceptive sensors to determine the agent’s pose and motion.
- **Sensor fusion**: combining multiple modalities (e.g., vision + depth + tactile) into a coherent representation.
- **Attention and saliency**: prioritizing relevant sensory input to reduce computational load and improve decision speed.

## Related Pages

- [[Perception]] ⚠️ – the broader process of interpreting sensory data.
- [[Sensor Fusion]] ⚠️ – algorithmic techniques for combining sensor streams.
- [[SLAM]] – simultaneous localization and mapping, a key algorithm enabled by sensing intelligence.
- [[Navigation Stack]] ⚠️ – a ROS‑based framework that implements sensing intelligence for mobile robots.

## Source

Based on content from `papers/2508.15354.pdf` (arXiv).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Sensing Intelligence` --[[related_to]] ⚠️--> `SLAM` _(wikilink)_
