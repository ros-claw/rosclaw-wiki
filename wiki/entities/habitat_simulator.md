---
id: habitat_simulator
title: Habitat simulator
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T04:33:44'
last_reinforced: '2026-04-30T04:33:44'
supersedes: []
sources:
- papers/2312.03275.pdf
source_type: arxiv_paper
---

# Habitat Simulator

## Overview

Habitat Simulator is a photorealistic 3D environment simulation platform designed for embodied AI research. It provides high-fidelity rendering and physics integration to support training and evaluation of agents in indoor and outdoor scenes. The simulator is built on the Habitat framework and is commonly used to benchmark navigation, manipulation, and vision-language grounding tasks.

## Capabilities

- **Photorealistic 3D environment simulation** – Renders high-quality visual observations with configurable sensors (RGB, depth, semantic, etc.).
- **Supports multiple large-scale datasets** – Can load and simulate scenes from **Gibson dataset**, **HM3D dataset**, and **MP3D dataset ⚠️ ⚠️**, enabling cross-dataset generalization studies.

## Relationships

- **Used by** – The Habitat Simulator is the evaluation backend for **VLFM** (Vision-Language Foundation Models), providing a consistent testbed across diverse 3D scenes.
- **Hosts** – It directly loads and manages scene assets from Gibson dataset, HM3D dataset, and MP3D dataset ⚠️ ⚠️, acting as a dataset integration layer.

## Usage

In the context of the VLFM system, Habitat Simulator supplies the interactive environment for goal-conditioned navigation and object search. Agents receive first-person RGB observations and perform actions (e.g., move, rotate, pick) while the simulator updates state and provides reward signals. This setup allows reproducible evaluation of embodied agents without requiring a physical robot.