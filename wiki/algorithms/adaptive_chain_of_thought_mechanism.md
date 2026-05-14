---
id: adaptive_chain_of_thought_mechanism
title: Adaptive Chain-of-Thought Mechanism
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:20'
last_reinforced: '2026-04-29T23:58:20'
supersedes: []
sources:
- papers/2601.08665.pdf
source_type: arxiv_paper
---

# Adaptive Chain-of-Thought Mechanism

The **Adaptive Chain-of-Thought (CoT) Mechanism** is an algorithm inspired by the dual-process theory of human cognition. It enables an embodied agent to fluidly switch between fast, intuitive execution and slow, deliberate planning — dynamically triggering explicit reasoning only when necessary. This reduces unnecessary reasoning overhead while preserving the ability to handle complex or novel scenarios.

## Parameters

- **Inspiration**: Dual-process theory of human cognition
- **Modes**:
  - Fast intuitive execution
  - Slow deliberate planning
- **Trigger condition**: Dynamically activated when explicit reasoning is required (e.g., when visual or temporal uncertainty is high)

## Capabilities

- Enables the agent to switch fluidly between intuitive and deliberate reasoning depending on the situation
- Reduces unnecessary reasoning overhead by avoiding continuous deep reasoning on routine tasks
- Supports robust performance across both familiar and unfamiliar navigation environments

## Relationships

- **Part of**: VLingNav
- **Uses**: Dual-process theory

## Motivation

Inspired by human cognitive dual-process theory, this mechanism was developed to handle both routine and novel navigation situations. In everyday navigation, most decisions can be made quickly and intuitively (System 1), but unfamiliar or ambiguous scenes require effortful, step-by-step reasoning (System 2). The adaptive mechanism mirrors this cognitive strategy.

## Operation

The mechanism triggers explicit chain-of-thought reasoning only when uncertainty in visual input or temporal sequence is high. During normal operation, the agent executes actions intuitively using learned policy priors. When visual ambiguity or temporal novelty is detected, a slow deliberate planning chain is activated to analyze the situation step by step. This dynamic gating between modes allows the agent to maintain efficiency while preserving the flexibility to handle edge cases.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Adaptive Chain-of-Thought Mechanism` --extends ⚠️--> `VLingNav`
