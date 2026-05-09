---
id: slam
title: SLAM
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:45:48'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.17792.pdf
source_type: arxiv_paper
---

## SLAM (Simultaneous Localization and Mapping)

**SLAM** (Simultaneous Localization and Mapping) is a fundamental algorithm in robotics and embodied AI that enables a robot to build a map of an unknown environment while simultaneously tracking its own location within that map. It is a core capability for autonomous navigation, exploration, and scene understanding.

### Capabilities

- **Reconstruct robot trajectories** — SLAM algorithms integrate sensor data (e.g., LiDAR, cameras, IMU) over time to estimate the full path traveled by the robot, producing a consistent trajectory even in drift-prone odometry.
- **Provide motion tendency references** — By analyzing the reconstructed trajectory and map, SLAM can infer the robot’s intended motion direction, speed, and behavioral patterns, serving as a reference for higher-level planning or world model training.

### Relationships

- **Used by** [[Target-Bench]] — SLAM provides the trajectory and mapping inputs required for benchmarking target-driven navigation tasks. In the context of [[Target-Bench]], SLAM‑derived trajectories are used as ground‑truth motion tendency references for evaluating the predictions of video world models.
- **Used by** [[Video World Models]] — SLAM-derived motion tendencies help condition or supervise video prediction models that learn physical dynamics from robot experience.

### Role in Target-Bench

SLAM‑based trajectories serve as ground‑truth motion tendency references for evaluating video world model predictions. This enables [[Target-Bench]] to assess whether a learned world model accurately captures the robot’s physical motion and spatial understanding, rather than relying solely on visual reconstruction fidelity.

### Context

SLAM is a mature field with many variants (EKF-SLAM, GraphSLAM, ORB-SLAM, etc.). In the context of the source paper (arxiv `2511.17792`), SLAM is employed as a preprocessing or grounding module to extract structured spatiotemporal information from raw sensor streams, which is then leveraged by video world models for downstream tasks such as planning and simulation. Its ability to produce high‑fidelity trajectory and motion cues makes it a reliable prior for learning‑based approaches. The use of SLAM as a ground‑truth reference in [[Target-Bench]] further underscores its value for benchmarking embodied AI systems.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SLAM` --[[used_by]] ⚠️ ⚠️--> `Target-Bench`
- `SLAM` --[[used_by]] ⚠️ ⚠️--> `Video World Models`