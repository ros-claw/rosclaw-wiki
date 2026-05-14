---
id: sg3d
title: SG3D
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:53'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

# SG3D

**SG3D** is a benchmark designed for Embodied Navigation tasks, focused on evaluating 3D scene understanding, generalization, and question‑answering capabilities. It provides a standardized environment and metrics to assess how well navigation agents can operate and answer queries in simulated 3D worlds.

## Capabilities

- **Embodied Navigation evaluation**: measures success rate, path efficiency, and generalization across diverse 3D scenes.
- **Question‑Answering evaluation**: tests agents’ ability to perceive and reason about the environment to answer semantic queries during navigation.

## Key Results

In the SG3D benchmark, the MTU3D architecture achieved a **9% improvement in success rate** over the previous state‑of‑the‑art (SOTA). This result was reported in the paper *"MTU3D: Multi‑Task Unified 3D Navigation"* (arXiv:2507.04047).

## Relationship Annotations

- **SG3D** → **Embodied Navigation**: A task for ⚠️ which SG3D serves as a benchmark.
- **SG3D** → **MTU3D**: evaluates ⚠️ the performance of MTU3D; MTU3D improves upon ⚠️ previous SOTA on SG3D. MTU3D uses ⚠️ SG3D as an evaluation platform.
- **SG3D** → **SOTA ⚠️**: compares against ⚠️ existing state‑of‑the‑art methods via the benchmark.
- **SG3D** → **3D Scene Understanding ⚠️**: The benchmark tests ⚠️ aspects of 3D scene understanding and perception.
- **SG3D** → **Embodied Question Answering ⚠️**: The benchmark extends ⚠️ to evaluating question‑answering in embodied contexts.

## Context

As a benchmark, SG3D enables reproducible comparison across embodied navigation and question‑answering algorithms. Its emphasis on 3D environments and semantic reasoning aligns with the growing need for robots to operate in realistic, non‑planar spaces while interacting through natural language. The 9% improvement by MTU3D highlights progress in integrating multiple navigation sub‑tasks (e.g., mapping, planning, and obstacle avoidance) into a unified model.