---
id: multi_turn_navigation
title: Multi-turn navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:17:10'
last_reinforced: '2026-04-30T03:17:10'
supersedes: []
sources:
- papers/2108.11544.pdf
source_type: arxiv_paper
---

# Multi-turn Navigation

**Multi-turn navigation** is a category of Vision-Language Navigation (VLN) tasks where navigation instructions are given multiple times, rather than as a single, monolithic instruction. This reflects real-world scenarios where a robot or agent receives incremental guidance, often after completing previous steps or when it reaches a landmark.

## Subtypes

Multi-turn navigation is subdivided into two main categories:

- **Passive navigation**: The agent receives instructions sequentially without being able to ask for clarification or interact with the instructor. The instructions are provided at pre-determined intervals or after the agent reaches certain waypoints.
- **Interactive navigation**: The agent can actively seek additional information, ask clarifying questions, or request further navigation commands based on its current state. This more closely mimics human-guided navigation.

## Relationship to Vision-Language Navigation

Multi-turn navigation is a sub-task (part of) Vision-Language Navigation (VLN). While classical VLN typically involves a single instruction describing the entire route, multi-turn navigation breaks the task into a natural dialogue-like sequence, enabling longer and more complex navigation episodes.

## Sources

- arxiv paper [2108.11544] — *"Multi-turn Navigation: A Survey and Benchmark"* (or similar title; content extracted from structured facts).