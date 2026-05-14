---
id: topological_graph_with_visitation_records
title: Topological Graph with Visitation Records
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:56:23'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.20499.pdf
source_type: arxiv_paper
---

# Topological Graph with Visitation Records

A **Topological Graph with Visitation Records** is a continuously updated spatial memory structure that captures the layout of an environment as a graph of waypoints, each annotated with visitation markers. It enables an embodied agent to maintain a persistent record of explored areas and plan future navigation paths by leveraging both topological connectivity and historical visitation data.

## Overview

In the context of zero-shot Visual Language Navigation (VLN), this graph serves as the agent’s internal map, built incrementally from observations. Each node represents a distinct location (waypoint), and edges encode traversable paths between them. Visitation records—such as timestamps, frequency, or success/failure flags—are stored alongside nodes, allowing the system to distinguish between explored, partially explored, and unexplored regions. This memory structure is critical for long-horizon exploration and efficient replanning.

The graph is parameterized by:
- **Nodes**: waypoints (positions)
- **Edges**: traversability between waypoints
- **Node attributes**: visitation count

## Construction

The graph is built incrementally as the agent moves. New waypoints from the predictor are added as nodes, and edges are created between nearby nodes if a straight-line path is obstacle-free. Each node stores a visitation count that increments when the agent passes through it. This process ensures the graph remains faithful to the physical topology of the environment while accumulating exploration history.

## Capabilities

- **Dynamically updated graph** capturing the topological structure of the environment
- **Explicit visitation records** that encode exploration history, enabling informed decision-making about where to go next
- **Captures global connectivity** of the environment
- **Tracks exploration history** for informed decision-making (e.g., which areas have been visited and how often)

## Relationships

- **Used by**: TopoGraph-and-VisitInfo-Aware Prompting — this prompting strategy feeds graph and visitation information into a language model to generate navigational commands.
- **Part of**: Zero-Shot VLN Framework with TopoGraph Prompting — the topological graph is a core component enabling the framework to perform navigation without prior training on specific environments.

## Usage

During a VLN episode, the graph is initialized empty and extended as the agent moves. After each step, new waypoints are added, and visitation counts for the current node are incremented. The resulting structure is then used by the TopoGraph-and-VisitInfo-Aware Prompting module to produce context-aware instructions, such as "go to the unexplored corridor to the left" or "return to the kitchen where you started." This allows the agent to exhibit systematic exploration rather than random wandering.

## Source

- Paper: `papers/2509.20499.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Topological Graph with Visitation Records` --related_to ⚠️--> `TopoGraph-and-VisitInfo-Aware Prompting` _(wikilink)_