---
id: coverage_weighted_by_length_score_cls
title: Coverage weighted by Length Score (CLS)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:07:19'
last_reinforced: '2026-04-30T03:07:19'
supersedes: []
sources:
- papers/1905.12255.pdf
source_type: arxiv_paper
---

# Coverage weighted by Length Score (CLS)

**Coverage weighted by Length Score (CLS)** is a metric proposed for evaluating instruction-following agents in embodied navigation tasks, particularly on the Room-to-Room (R2R) Dataset. Unlike traditional goal-completion metrics that only assess whether an agent reaches the final target location, CLS measures **how faithfully the agent follows the entire sequence of instructions** by weighting the agent’s path coverage relative to the length of the natural-language instruction.

## Overview

CLS addresses a fundamental shortcoming of existing metrics for the Room-to-Room dataset: an agent that reaches the goal via an unlisted or circuitous route — or even by ignoring the verbal guidance entirely — may still achieve a high goal-completion score. CLS penalizes such deviations by computing a coverage score that compares the agent’s traversed path to the ideal path implied by the instructions, normalized by the instruction length. A higher CLS indicates stronger alignment between the agent’s behavior and the literal command.

## Capabilities

- **Measures instruction fidelity** by weighting coverage of the path relative to the instruction length.
- **Addresses shortcomings of goal-completion metrics** for the Room-to-Room (R2R) Dataset, providing a more nuanced evaluation of embodied instruction-following.

## Relationship to Other Metrics

- **supersedes** [Existing metrics for R2R] — CLS supersedes earlier R2R evaluation metrics (e.g., success rate, navigation error) by introducing an instruction-fidelity component.

## Usage

CLS is commonly used alongside traditional metrics (e.g., success rate, path length) to holistically evaluate Vision-Language Navigation (VLN) agents. It is especially relevant for systems trained on the R2R dataset and is cited in subsequent VLN benchmarks and model analyses.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Coverage weighted by Length Score (CLS)` --implements ⚠️--> `Room-to-Room (R2R) Dataset`
