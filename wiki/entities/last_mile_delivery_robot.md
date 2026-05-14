---
id: last_mile_delivery_robot
title: Last-Mile Delivery Robot
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T23:59:58'
last_reinforced: '2026-04-29T23:59:58'
supersedes: []
sources:
- papers/2512.09607.pdf
source_type: arxiv_paper
---

# Last-Mile Delivery Robot

## Overview

A **last-mile delivery robot** is an autonomous mobile platform designed to transport goods from a distribution hub (e.g., a delivery van or local depot) directly to a customer’s doorstep. These robots operate in urban environments, navigating sidewalks, crosswalks, and building entrances while handling diverse pedestrian traffic and unpredictable obstacles. The target application domain is **urban logistics**, where reliability and adaptability are critical.

## Parameters

- **Application domain**: urban logistics  
- **Navigation requirement**: language-guided navigation in unfamiliar cities – the robot must interpret free-form human instructions (e.g., "take the third left after the blue awning") to reach a drop-off point without relying on a pre‑mapped route.

## Capabilities

- **Follow free-form language instructions**: the robot can parse natural‑language commands and translate them into actionable waypoints or navigation commands.  
- **Operate in real‑world urban environments**: it must cope with dynamic conditions such as moving vehicles, construction zones, weather changes, and varying sidewalk widths.

## Relationships

- **Uses** → UrbanNav: The last‑mile delivery robot is cited as a representative autonomous agent that would benefit from the UrbanNav framework, which enables language‑guided urban navigation in previously unvisited city districts.

## Context

As described in the source paper (`papers/2512.09607.pdf`), the last‑mile delivery robot exemplifies the class of agents that require robust, instruction‑following navigation to succeed in real‑world last‑mile delivery tasks. UrbanNav’s approach directly addresses the challenges these robots face when operating beyond familiar, pre‑mapped environments.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Last-Mile Delivery Robot` --related_to ⚠️--> `language-guided navigation`
- `Last-Mile Delivery Robot` --uses ⚠️--> `UrbanNav`
