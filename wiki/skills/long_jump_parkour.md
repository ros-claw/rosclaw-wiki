---
id: long_jump_parkour
title: Long jump (parkour)
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T04:30:19'
last_reinforced: '2026-04-30T04:30:19'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# Long jump (parkour)

A parkour skill enabling a robot to perform a dynamic horizontal leap across a gap, covering a distance of up to 2× its own body length. This skill is a fundamental building block for more complex parkour sequences and requires precise coordination of thrust, posture, and landing absorption.

## Description

The robot performs a long jump across gaps twice its own body length, demonstrating precise control over horizontal distance and landing. The skill involves a running approach, a powerful takeoff at the edge of the gap, a controlled flight phase, and a stable landing on the far side.

## Parameters

| Parameter | Value |
|-----------|-------|
| Distance ratio | 2× robot length |
| Gap type | Horizontal gap |

## Capabilities

- Dynamic horizontal leap across gap

## Relationships

- **Performed by**: [[Extreme Parkour Robot]]
- **Controlled by**: [[Extreme Parkour Policy]] (the policy outputs the joint trajectories and timing required to execute this skill)

*Source: arxiv 2309.14341*