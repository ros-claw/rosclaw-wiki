---
id: high_level_planner
title: High-Level Planner
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:36:22'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2601.04699.pdf
source_type: arxiv_paper
---

# High-Level Planner

## Summary

A component of SeqWalker that decomposes long-horizon instructions into sub‑instructions relevant to the current observation.

## Overview

The **High-Level Planner** is a core module within the SeqWalker architecture responsible for dynamic sub‑instruction selection. It receives global instructions ⚠️ and current visual observations ⚠️, then outputs the most contextually relevant sub‑instructions ⚠️ to guide the agent’s low‑level actions. By filtering irrelevant information in real time, the planner reduces the cognitive load on downstream components and sharpens the agent’s attention toward observationally important details. This decomposition of long‑horizon instructions into sub‑instructions grounded in the current visual context is essential for efficient task execution.

## Parameters

| Parameter | Description |
|-----------|-------------|
| **Role** | Dynamic sub‑instruction selection |
| **Input** | Global instructions, current visual observations |
| **Output** | Contextually relevant sub‑instructions |

## Capabilities

- **Reduce cognitive load** – Eliminates extraneous instructions that are not applicable to the current scene, preventing the agent from being overwhelmed.
- **Improve attention** – Enhances the agent’s focus on observationally relevant details by supplying only the sub‑instructions that align with the current visual context.
- **Dynamic selection** – Continuously selects which global instructions to decompose into sub‑instructions based on real‑time visual input.

## Relationships

- **Part of** SeqWalker — the High‑Level Planner is one of the core modules within the SeqWalker system.
- **Uses** Global Instructions ⚠️ as high‑level guidance.
- **Uses** Visual Observations ⚠️ from the environment to ground instruction selection in real‑time perception.

_Source: arxiv:2601.04699_