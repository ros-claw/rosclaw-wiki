---
id: particle_filter_coarse_localization
title: Particle Filter Coarse Localization
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:34:41'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2602.19308.json
- articles/wildos.md
source_type: arxiv_paper
---

---

# Particle Filter Coarse Localization

**Type**: Algorithm  
**Source**: [[arXiv:2602.19308]] ⚠️ (WildOS paper), supplemented by WildOS blog post

## Overview

**Particle Filter Coarse Localization** is a localization algorithm designed for navigation toward distant semantic goals. Unlike traditional particle filters that require a global map and precise sensor measurements, this algorithm estimates candidate goal positions beyond the robot's depth-sensing horizon using only an open-vocabulary target query and image observations. It is a core component of the [[WildOS]] system for long-range exploration.

This method enables a robot to reason about where a semantically described object (e.g., "a red mailbox") is located across a large environment, even when the object is not immediately visible or within range of onboard depth sensors. The output is a coarse 3D target location beyond direct sensor range.

## Method

A particle filter maintains a distribution over possible goal locations. Each particle represents a candidate position in the robot's internal navigation graph. The weight of each particle is computed based on an **object similarity score** derived from [[ExploRFM]], which compares the open-vocabulary query to observations at that position. Over time, particles converge to regions that are semantically consistent with the target query.

More specifically, the algorithm performs **probabilistic goal triangulation from multiple viewpoints**. Object detections from several vantage points are fused probabilistically to estimate a coarse 3D target location beyond direct sensor range. Projected particles represent the uncertainty in this goal location.

This approach allows the robot to drive toward areas of high semantic likelihood, progressively refining its estimate as new observations become available. The coarse localization output feeds into downstream planning modules for reaching the distant goal.

## Operation

Object detections from multiple viewpoints are fused by a probabilistic goal triangulation module to estimate a coarse 3D target location beyond direct sensor range. Projected particles represent goal location uncertainty.

## Parameters

| Parameter | Description |
|-----------|-------------|
| **Type** | Localization algorithm for distant goals |
| **Method** | Probabilistic goal triangulation from multiple viewpoints (particle filter) |
| **Input** | Open-vocabulary target query, image observations |
| **Output** | Coarse 3D target location beyond direct sensor range |

## Capabilities

- Estimates coarse 3D positions for distant objects without a global map
- Scales to long-range exploration (beyond sensor horizon)
- Works with arbitrary open-vocabulary queries (not limited to pre-defined classes)
- Enables planning toward distant semantic goals

## Relationships

- **Part of**: [[WildOS]]
- **Depends on**: [[Object similarity scoring]] ⚠️ from [[ExploRFM]]
- **Enables**: [[Planning toward distant goals]] ⚠️ (navigation to semantically identified locations)

## See Also

- [[Particle Filter]] ⚠️ (general algorithm)
- [[Coarse-to-fine localization]] ⚠️
- [[Long-horizon semantic navigation]] ⚠️
- [[WildOS]] (system architecture)
- [[ExploRFM]] (similarity scoring backbone)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Particle Filter Coarse Localization` --[[extends]] ⚠️ ⚠️--> `WildOS`
- `Particle Filter Coarse Localization` --[[extends]] ⚠️ ⚠️--> `ExploRFM`