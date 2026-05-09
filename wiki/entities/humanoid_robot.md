---
id: humanoid_robot
title: Humanoid Robot
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:34:13'
last_reinforced: '2026-04-29T21:34:13'
supersedes: []
sources:
- papers/2510.07152.pdf
source_type: arxiv_paper
---

## Overview

A **full‑sized humanoid robot** capable of terrain‑aware locomotion using a **depth‑only perceptive framework ([[DPL (Depth-only Perceptive Locomotion) Framework]] ⚠️ ⚠️ ⚠️)**. The robot is the physical platform evaluated in the context of agile and adaptive locomotion across diverse and challenging terrains, relying solely on depth sensor input for perception.

This embodiment is at the center of the DPL approach, which enables real‑time adaptation without explicit terrain classification or an onboard map.

## Capabilities

- **Agile and adaptive locomotion** across diverse and challenging terrains (e.g., slopes, stairs, obstacles, deformable ground).
- **Terrain‑aware perceptive locomotion** using depth‑only visual input; no RGB or semantic segmentation required.

## Relationships

- **uses**: [[DPL (Depth-only Perceptive Locomotion) Framework]] ⚠️ ⚠️ ⚠️ – the full‑sized humanoid robot serves as the test‑bed for the depth‑only locomotion policy.

## Related Pages

- [[DPL (Depth-only Perceptive Locomotion) Framework]] ⚠️ ⚠️ ⚠️
- [[Humanoid Locomotion]] ⚠️
- [[Perceptive Control]] ⚠️