---
id: run_across_tilted_ramps_parkour
title: Run across tilted ramps (parkour)
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T04:31:21'
last_reinforced: '2026-04-30T04:31:21'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# Run Across Tilted Ramps (Parkour)

The **Run across tilted ramps** skill enables a robot to perform dynamic locomotion across slanted surfaces, simulating parkour-style traversal on inclined ramps. It is a core capability demonstrated by the [[Extreme Parkour Robot]] under the control of the [[Extreme Parkour Policy]]. The skill emphasizes stability, agility, and adaptability on non-flat terrain.

## Parameters

| Parameter | Value |
|-----------|-------|
| Surface type | tilted ramp |
| Speed | dynamic running |

## Capabilities

- Dynamic locomotion on inclined non-flat surfaces
- Adaptive foot placement and body alignment on slopes
- Continuous running without loss of stability

## Relationships

- **Performed by**: [[Extreme Parkour Robot]] (implements)
- **Controlled by**: [[Extreme Parkour Policy]] (depends_on)

## Description

The robot runs across tilted ramps, maintaining dynamic stability on sloped surfaces. This showcases adaptability to varying terrain orientations. The policy must compensate for gravitational asymmetry and shifting center of mass, requiring real‑time adjustment of gait parameters. Successful execution demonstrates the robot’s ability to handle real‑world unstructured environments where flat ground is not guaranteed.

## Source

This skill is derived from the paper *Extreme Parkour: Learning Agile Locomotion on Challenging Terrain* (arXiv:2309.14341).