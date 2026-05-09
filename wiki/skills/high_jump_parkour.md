---
id: high_jump_parkour
title: High jump (parkour)
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T04:29:38'
last_reinforced: '2026-04-30T04:29:38'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# High Jump (Parkour)

## Overview

The **high jump** is a dynamic parkour skill that enables a robot to clear vertical obstacles up to twice its own height. It requires precise timing, force control, and a robust control policy to generate sufficient upward and forward momentum while maintaining stability on landing.

## Parameters

- **Height ratio**: 2× robot height
- **Obstacle type**: vertical obstacle

## Capabilities

- Dynamic vertical jump over obstacle

## Relationships

- **Performed by**: [[Extreme Parkour Robot]]
- **Controlled by**: [[Extreme Parkour Policy]]

## Description

The robot executes a high jump to clear obstacles twice its own height. This is a highly dynamic maneuver requiring precise timing and force control. The control policy must coordinate leg thrust, body orientation, and landing absorption to avoid collision or fall.

## Source

- arxiv paper: `papers/2309.14341.pdf`