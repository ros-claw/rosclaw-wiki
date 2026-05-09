---
id: localization_grounded_navigation
title: Localization-grounded navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:22:41'
last_reinforced: '2026-04-30T03:22:41'
supersedes: []
sources:
- papers/2512.19629.pdf
source_type: arxiv_paper
---

## Overview

**Localization-grounded navigation** is a [[navigation]] ⚠️ paradigm that implicitly estimates the robot's pose from visual geometry, rather than relying on a separate localization module with accurately calibrated sensors. By grounding navigation decisions in metric-scale geometric cues (e.g., depth from single images or visual odometry), this approach reduces the dependency on precise extrinsic calibration and improves generalization across different robot platforms and environments.

## Context

Traditional navigation pipelines decouple localization, mapping, and planning. Localization modules — whether filter-based (e.g., [[Extended Kalman Filter]] ⚠️) or optimization-based (e.g., [[factor graph optimization]] ⚠️) — require accurate extrinsic calibration between sensors (e.g., camera-to-LiDAR or camera-to-base transforms). In unstructured or dynamic environments, calibration drift or sensor misalignment leads to cascading errors that degrade planning performance. **Localization-grounded navigation** replaces these brittle modular estimators with learned representations that encode metric-scale geometry directly from visual input, enabling end-to-end planning without explicit state estimation.

## Capabilities

- **Reduced dependency on sensor calibration** – By learning the mapping from raw images to navigation-relevant geometry, the system becomes robust to calibration inaccuracies or changes in sensor mounting.
- **Improved generalization across robots and environments** – The learned implicit representation can adapt to different camera intrinsics, robot kinematics, and scene geometries without retuning calibration parameters.
- **Mitigation of cascading errors** – Modular pipelines pass localization uncertainty from block to block; grounding navigation in visual geometry avoids amplifying errors from separate stages.

## Relationships

- **Implemented by** → [[LoGoPlanner]] – A concrete planner that realizes localization-grounded navigation by using learned metric-scale visual features to guide trajectory generation.
- **Related to** → [[End-to-end learning]] – Shares the philosophy of replacing hand-designed modules with differentiable representations, though localization-grounded navigation retains planning structure; also related to [[Implicit state estimation]] ⚠️, where the system learns an internal representation of pose without explicit filtering.

## Sources

- [[data/raw/papers/2512.19629.pdf]] ⚠️ – arxiv paper introducing LoGoPlanner and the localization-grounded navigation concept.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Localization-grounded navigation` --[[related_to]] ⚠️--> `LoGoPlanner` _(wikilink)_
