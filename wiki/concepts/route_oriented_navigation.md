---
id: route_oriented_navigation
title: Route-oriented navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:18:53'
last_reinforced: '2026-04-30T03:18:53'
supersedes: []
sources:
- papers/2108.11544.pdf
source_type: arxiv_paper
---

**Route-oriented navigation** is a subtype of Single-turn navigation where instructions specify a sequence of multiple locations rather than a single destination. Unlike point-to-point navigation (e.g., “go to the kitchen”), route-oriented tasks require the agent to traverse an ordered list of waypoints (e.g., “go to the kitchen, then the living room, then the bedroom”). This makes the task more challenging because the agent must maintain context across subgoals and plan a path that visits all specified locations in order.

Route-oriented navigation is typically evaluated in vision-and-language navigation (VLN) benchmarks where instructions describe a multi-step path. The agent must understand the sequential nature of the command and execute the actions in the correct order.

### Relationships
- **subtype_of** Single-turn navigation — inherits the single-turn (non-interactive) format but adds sequential subgoal specification.