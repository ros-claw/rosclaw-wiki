---
id: transformer_based_cross_modal_planner
title: Transformer-based Cross-modal Planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:03:28'
last_reinforced: '2026-04-29T21:03:28'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

## Overview

The **Transformer-based Cross-modal Planner** is a planning module that serves as a core component of the ETPNav framework. It fuses visual information from a Topological Map ⚠️ with textual Language Instructions ⚠️ to generate a high-level Navigation Plan ⚠️ composed of a sequence of subgoals.

## Capabilities

- Fuses visual and textual information via cross-modal attention.
- Generates high-level navigation plans in the form of subgoal sequences.

## Architecture & Design

The planner employs a Transformer ⚠️ ⚠️ backbone with Cross-modal Attention ⚠️ ⚠️ to align language instructions with nodes of the topological map. This alignment allows the model to produce a coherent sequence of subgoals that guides the robot toward the goal specified by the instructions.

## Parameters

- **Type**: planning module
- **Backbone**: Transformer
- **Input**: topological map + language instructions
- **Output**: navigation plan (sequence of subgoals)

## Relationships

- **Part of**: ETPNav
- **Uses**: Transformer ⚠️ ⚠️, Cross-modal Attention ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Transformer-based Cross-modal Planner` --extends ⚠️--> `ETPNav`
