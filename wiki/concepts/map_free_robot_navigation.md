---
id: map_free_robot_navigation
title: Map-free robot navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:31:09'
last_reinforced: '2026-04-29T21:31:09'
supersedes: []
sources:
- papers/2403.06828.pdf
source_type: arxiv_paper
---

# Map-free Robot Navigation

## Overview

**Map-free robot navigation** is a paradigm that enables a robot to operate in unknown, unstructured environments without requiring an explicit pre-built or concurrently constructed map. Instead of relying on traditional SLAM pipelines, map-free approaches use direct sensor data — such as raw point clouds — to inform motion planning in real time. The technique is exemplified by **[[NeuPAN]]**, which achieves map-free navigation by mapping raw point clouds into a latent distance feature space, allowing the robot to adapt to arbitrarily shaped objects and navigate without constructing or storing an environmental map.

## Parameters

| Parameter     | Value                              |
|---------------|------------------------------------|
| Type          | Navigation paradigm                |
| Core feature  | No prior map required              |
| Environment   | Unknown, unstructured              |

## Capabilities

- Navigate without building or maintaining explicit maps.
- Adapt to arbitrarily shaped objects during motion.
- Operate directly from sensor observations (e.g., point clouds, depth images).

## Relationships

- **Used by** → [[NeuPAN]] (implements map-free navigation through learned latent distance fields).
- **Contrasts with** → [[SLAM-based navigation]] ⚠️ (which relies on concurrent map building and localization).

## Description

Map-free navigation uses direct sensor data (e.g., point clouds) for motion planning without constructing an environmental map. [[NeuPAN]] achieves this by mapping raw point clouds to a latent distance feature space, enabling real‑time obstacle avoidance and path planning in previously unseen environments. This approach reduces the computational overhead of map maintenance and is particularly suited for agile, unstructured settings where map building is impractical or impossible.

## Sources

- arxiv paper: `papers/2403.06828.pdf` (NeuPAN: End-to-End Map-Free Navigation)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Map-free robot navigation` --[[related_to]] ⚠️--> `NeuPAN` _(wikilink)_
