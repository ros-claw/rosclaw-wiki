---
id: semantic_utility_driven_subgoal_selection
title: Semantic Utility-Driven Subgoal Selection
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:56:05'
last_reinforced: '2026-04-29T20:56:05'
supersedes: []
sources:
- papers/2509.20739.pdf
source_type: arxiv_paper
---

# Semantic Utility-Driven Subgoal Selection

## Definition

Semantic Utility-Driven Subgoal Selection is an algorithm within the Decision-Driven Semantic Object Exploration (DD-SOE) framework. It defines how a robot chooses its next exploration target by evaluating a semantic utility function that balances semantic relevance, reliability, and reachability. The goal is to maximize information gain and task relevance while ensuring physical feasibility.

## Purpose

Uses a semantic utility function to choose subgoals that maximize the information gain and task relevance while ensuring the robot can physically reach the target.

## Capabilities

- Select exploration targets balancing semantic relevance, reliability, and reachability
- Prioritize subgoals based on semantic utility

## Relationships

- **part_of** Decision-Driven Semantic Object Exploration (DD-SOE) — this algorithm is a core component of the overall exploration framework, responsible for the decision-making step that selects the next semantic subgoal to pursue.

## Related Concepts

- Semantic Utility ⚠️ — the metric computed by this algorithm to rank candidate subgoals.
- Subgoal Selection ⚠️ — general problem of choosing intermediate targets in autonomous exploration.
- Reachability Analysis ⚠️ — the algorithm ensures selected targets are physically accessible.
- Information Gain ⚠️ — one of the factors balanced by the utility function.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Semantic Utility-Driven Subgoal Selection` --extends ⚠️--> `Decision-Driven Semantic Object Exploration (DD-SOE)`
