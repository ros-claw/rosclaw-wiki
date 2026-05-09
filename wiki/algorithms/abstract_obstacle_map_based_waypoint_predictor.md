---
id: abstract_obstacle_map_based_waypoint_predictor
title: Abstract Obstacle Map-Based Waypoint Predictor
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:55:08'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.20499.pdf
source_type: arxiv_paper
---

# Abstract Obstacle Map-Based Waypoint Predictor

## Overview

The **Abstract Obstacle Map-Based Waypoint Predictor** is a **simplified predictive module** within the [[Zero-Shot VLN Framework with TopoGraph Prompting]] that generates **linearly reachable waypoints** from an abstract representation of obstacles. It enables local path planning by converting a high-level obstacle map into discrete, navigable points that can be executed by a robot or agent. The predictor reduces the search space and provides structured inputs for the language model. It is designed to integrate with a [[Multimodal Large Language Model]] ⚠️ for vision-language navigation tasks, allowing the agent to decide upon and follow a sequence of waypoints without prior training on specific environments.

## Description

This waypoint predictor operates on a compressed obstacle map derived from sensor data. It identifies linearly reachable points, which are then fed into the MLLM for selection. The predictor reduces the search space and provides structured inputs for the language model, enabling zero-shot generalization.

## Input and Output

- **Input**: An [[Abstract Obstacle Map]] — a compressed, symbolic representation of environmental obstacles derived from sensor data or scene graphs.
- **Output**: A set of **linearly reachable waypoints** — positions in the environment that can be reached via straight-line trajectories without collision, given the obstacle map.

## Capabilities

- Generates reachable waypoints from an abstract obstacle map representation, facilitating local navigation.
- Enables local path planning by providing candidate navigation targets.
- Integrates with a multimodal large language model for high-level navigation planning, bridging perception and action.

## Operation

The predictor processes the abstract obstacle map and outputs waypoints, which are then incorporated into a dynamically updated [[Topological Graph with Visitation Records]]. This graph maintains a record of visited locations and connectivity, enabling the system to avoid revisiting dead ends and to plan efficient routes. The waypoints serve as intermediate goals that the agent can follow sequentially, guided by the language model’s reasoning.

## Dependencies and Relationships

- **Uses**: [[Abstract Obstacle Map]]
- **Depends on**: [[Topological Graph with Visitation Records]]
- **Part of**: [[Zero-Shot VLN Framework with TopoGraph Prompting]] (also referred to as the Zero-Shot VLN Framework)

The predictor is a key module that bridges perception (obstacle map) and planning (topological graph), enabling zero-shot generalization to unseen environments.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Abstract Obstacle Map-Based Waypoint Predictor` --[[based_on]] ⚠️ ⚠️--> `Abstract Obstacle Map`
- `Abstract Obstacle Map-Based Waypoint Predictor` --[[based_on]] ⚠️ ⚠️--> `Topological Graph with Visitation Records`