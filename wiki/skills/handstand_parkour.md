---
id: handstand_parkour
title: Handstand (parkour)
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T04:30:49'
last_reinforced: '2026-04-30T04:30:49'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

## Description

The robot performs a **handstand** — an inverted stance on its hands (or equivalent front limbs) — requiring precise dynamic stabilization and exceptional balance under inverted dynamics. This skill demonstrates high-level parkour capability, pushing the limits of full-body control.

## Parameters

| Parameter | Value |
|-----------|-------|
| Maneuver type | Inverted stance on hands |
| Required balance | Dynamic stabilization |

## Capabilities

- Inverted static balance

## Relationships

- **Performed by**: Extreme Parkour Robot
- **Controlled by**: Extreme Parkour Policy

The skill `depends_on` the Extreme Parkour Policy for core control and `uses` the Extreme Parkour Robot's hardware to execute. It is `part_of` a broader parkour repertoire.

## Sources

- arXiv paper: [2309.14341](https://arxiv.org/abs/2309.14341) — raw file: `data/raw/papers/2309.14341.pdf`