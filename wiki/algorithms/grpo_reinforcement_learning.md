---
id: grpo_reinforcement_learning
title: GRPO reinforcement learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:50:06'
last_reinforced: '2026-04-29T20:50:06'
supersedes: []
sources:
- papers/2511.17889.pdf
source_type: arxiv_paper
---

# GRPO (Group Relative Policy Optimization)

## Definition

GRPO (Group Relative Policy Optimization) is a reinforcement learning algorithm designed to enhance reasoning consistency, control stability, and long-horizon execution in embodied policies. It operates by optimizing a policy relative to a group of sampled trajectories, promoting more reliable decision-making across sequential tasks.

## Usage in Embodied AI

GRPO is used by [[MobileVLA-R1]] as the second stage in a two-stage training paradigm. After supervised [[Chain-of-Thought (CoT)]] alignment, GRPO is applied to further improve the policy's reasoning and control stability. This approach enables the agent to maintain coherent reasoning across extended action sequences, addressing common failure modes in long-horizon manipulation and navigation tasks.

## Key Characteristics

- **Type**: Reinforcement learning algorithm for reasoning consistency
- **Primary capabilities**:
  - Enhances reasoning consistency across steps
  - Improves control stability during execution
  - Enables robust long-horizon task completion

## Architecture Context

GRPO depends_on [[reinforcement learning]] principles and implements group‑relative advantage estimation rather than absolute value functions. It part_of a two-stage training paradigm that first aligns the model via [[Supervised Fine-Tuning (SFT)]] or CoT distillation, then refines it with GRPO for execution robustness.

## Relationship Summary

| Entity | Relationship |
|---|---|
| [[MobileVLA-R1]] | `used_by` — GRPO serves as the RL stage in MobileVLA-R1's training |
| Two‑stage training paradigm | `part_of` — GRPO forms the second stage after CoT alignment |

## Source

- ArXiv paper: MobileVLA-R1 (2511.17889)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GRPO reinforcement learning` --[[extends]] ⚠️--> `MobileVLA-R1`
