---
id: multi_object_navigation_multion
title: Multi-Object Navigation (MultiON)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:50:09'
last_reinforced: '2026-04-29T20:50:09'
supersedes: []
sources:
- papers/2505.13729.pdf
source_type: arxiv_paper
---

# Multi-Object Navigation (MultiON)

## Overview

**Multi-Object Navigation (MultiON)** is a [[navigation]] ⚠️ task in which a team of robots must efficiently locate and reach multiple distinct objects in an unknown environment, without prior knowledge of object positions. It is designed to evaluate collaborative exploration and exploitation strategies, particularly when robots possess heterogeneous capabilities.

## Task Definition

In MultiON, the goal is to search for and navigate to several different objects as quickly as possible. The task challenges robots to:
- Coordinate their exploration to minimize redundant coverage.
- Leverage complementary sensing, mobility, or manipulation strengths.
- Adapt their search strategies based on real-time discoveries.

MultiON is a multi-agent extension of [[Object Navigation]] ⚠️ ⚠️ and serves as a benchmark for heterogeneous robot team coordination.

## Key Characteristics

| Property | Description |
|----------|-------------|
| *Task type* | Navigation (multi-target) |
| *Goal* | Search multiple different objects in unknown environments |
| *Agents* | Multi-robot team |
| *Environment* | Unknown, static or dynamic |

## Capabilities Tested

- **Complementary strength utilization** – agents with different sensors or actuation must collaborate to cover diverse object search spaces.
- **Team collaboration efficiency** – evaluates how well robots share information, assign targets, and avoid conflict.
- **Adaptive planning** – robots must replan based on partial observations (e.g., one robot finds a target, others adapt).

## Relationship to Other Concepts

- **Implements**: [[Object Navigation]] ⚠️ ⚠️ – MultiON generalizes single-object navigation to multiple, unseen objects.
- **Used by**: [[SayCoNav]] (SayCan+Navigation) – a recent embodied agent that employs language-conditioned policies for MultiON tasks.
- **Depends on**: [[Multi-Agent Coordination]] ⚠️ and [[Exploration vs. Exploitation]] ⚠️.

## Source

This page is based on arxiv paper **2505.13729** ( *SayCoNav: Language-Conditioned Multi-Object Navigation with Heterogeneous Robots* ), which introduces MultiON as a testbed for collaborative, heterogeneous robot teams.

## See Also

- [[Object Goal Navigation]]
- [[Embodied AI Benchmarks]] ⚠️
- [[Heterogeneous Robot Teams]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Multi-Object Navigation (MultiON)` --[[related_to]] ⚠️--> `SayCoNav` _(wikilink)_
