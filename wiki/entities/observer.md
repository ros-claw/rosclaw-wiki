---
id: observer
title: Observer
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:57:38'
last_reinforced: '2026-04-30T02:57:38'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

# Observer

The **Observer** is a virtual agent within the Where Are You? Dataset. It is spawned at a random location inside a 3D Environment ⚠️ and is responsible for navigating that environment using only first-person views. The Observer's primary role is to answer spatial questions posed by the Locator, thus enabling the dataset to study embodied question answering and grounded navigation.

## Role

The Observer functions as a mobile sensor platform: it moves from a first‑person perspective within the environment and responds to queries from the Locator. The agent’s perception is limited to egocentric visual input, and its actions are driven by the need to locate or identify objects, positions, or paths as requested. This design simulates a real‑world scenario in which an embodied agent must situate itself and provide information about its surroundings.

## Capabilities

- **Navigate in 3D environments**: The Observer can move through complex, procedurally generated spaces, planning paths and avoiding obstacles.
- **Answer questions from the Locator**: The Observer interprets natural‑language requests (e.g., “Where are you relative to the blue cube?”) and produces accurate responses based on its current position and visual observations.

## Relationships

- **Part of**: The Observer is a core component of the Where Are You? Dataset.
- **Interacts with**: The Observer engages in a question‑answer loop with the Locator, receiving queries and returning answers.
- **Depends on**: The Observer depends on the environment model (including geometry, lighting, and object placements) provided by the dataset for its navigation and perception tasks.
- **Uses**: The Observer uses first‑person camera views – corresponding to what a real robot or human would see – as its sole perceptual input.

## Source

This page is based on the paper *Where Are You? Building a grounded question‑answering dataset for embodied agents* (arXiv:2011.08277).