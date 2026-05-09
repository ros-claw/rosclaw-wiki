---
id: seenav_agent
title: SeeNav-Agent
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:25'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

# SeeNav-Agent

**Type:** Entity (Agent)  
**Confidence:** 0.85 *(reinforced by arxiv paper)*  
**Source:** `papers/2512.02631.pdf`

## Overview

SeeNav-Agent is a novel **Vision-Language Navigation (VLN)** agent framework designed to address persistent issues in perception, reasoning, and planning errors that plague [[LVLM]] ⚠️ ⚠️ ⚠️-based VLN agents. It introduces two key innovations: a **dual-view Visual Prompt (VP)** structure and a **step-level reinforcement fine-tuning** method called **Step Reward Group Policy Optimization (SRGPO)**. The dual‑view VP reduces perception hallucinations by encoding both an egocentric “what I see” perspective and a top‑down “where I am” layout; the step‑level reward mechanism improves planning by assigning credit for correct intermediate actions.

SeeNav-Agent demonstrates significant improvements over existing state-of-the-art methods on the [[EmbodiedBench Navigation]] ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ benchmark, particularly when paired with large foundation models like [[GPT-4.1]] or smaller post‑trained models like [[Qwen2.5-VL-3B]].

## Method

The framework operates in two complementary phases:

1. **Visual Prompt (VP)** – A dual‑view representation that provides richer spatial context and landmark understanding than single‑view prompts. This directly reduces perceptual hallucinations common in end‑to‑end LVLM navigation.
2. **Step‑level Reinforcement Fine‑tuning (SRGPO)** – A policy optimization method that operates at the step granularity rather than the full trajectory. By rewarding correct intermediate actions, SRGPO reduces compounding errors and improves final navigation success.

## Capabilities

- Reduces perception hallucinations via dual‑view visual prompt.
- Improves planning capability via step‑level reinforcement fine‑tuning.
- Achieves state‑of‑the‑art navigation success rates on [[EmbodiedBench Navigation]] ⚠️ ⚠️ ⚠️ ⚠️ ⚠️.

| Metric | Value | Model |
|--------|-------|-------|
| Navigation success rate (EmbodiedBench) | **86.7%** | [[GPT-4.1]] |
| Navigation success rate (EmbodiedBench) | **72.3%** | [[Qwen2.5-VL-3B]] (after [[SRGPO]] ⚠️ post‑training) |

- The GPT‑4.1 result surpasses the best [[LVLM]] ⚠️ ⚠️ ⚠️ baseline by approximately **20 percentage points**.
- The Qwen2.5‑VL‑3B result demonstrates that even a smaller 3B model can be dramatically improved (from a lower baseline) via step‑level reinforcement fine‑tuning.

## Relationships

- **uses** [[Visual Prompt (VP)]]
- **uses** [[Step Reward Group Policy Optimization (SRGPO)]]
- **uses** [[GPT-4.1]]
- **uses** [[Qwen2.5-VL-3B]]
- **depends_on** [[Large Vision-Language Models]] ⚠️ (specifically GPT‑4.1, Qwen2.5‑VL‑3B)
- **depends_on** [[Reinforcement Fine-Tuning (RFT)]]
- **implements** [[Vision-Language Navigation (VLN)]] agent paradigm
- **evaluated_on** [[EmbodiedBench Navigation]] ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ benchmark

## Key Advantages

- Reduces perception, reasoning, and planning errors that are common in end‑to‑end LVLM‑based VLN agents.
- Dual‑view VP provides richer spatial awareness than single‑view prompts, mitigating hallucination.
- Step‑level rewards in SRGPO allow more granular credit assignment compared to trajectory‑level reinforcement learning.

## Discussion Points

The 20‑point improvement over the best prior LVLM method suggests that the combination of structured visual prompting and step‑wise reinforcement is particularly effective for the VLN task. The success with a 3B‑scale model also hints at practical deployment on edge devices if further optimized. SeeNav-Agent is evaluated on the [[EmbodiedBench Navigation]] ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ benchmark, which includes diverse indoor environments and tasks.

## See Also

- [[GPT-4.1]]
- [[Qwen2.5-VL-3B]]
- [[Visual Prompt]] ⚠️
- [[Step Reward Group Policy Optimization (SRGPO)]]
- [[LVLM]] ⚠️ ⚠️ ⚠️ (Large Vision‑Language Model)
- [[Vision-Language Navigation]]
- [[EmbodiedBench Navigation]] ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
- [[Reinforcement Fine-Tuning (RFT)]]