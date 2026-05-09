---
id: multi_turn_qa_data_from_human_demonstrations
title: Multi-turn QA Data from Human Demonstrations
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:41:05'
last_reinforced: '2026-04-29T20:41:05'
supersedes: []
sources:
- papers/2504.09000.pdf
source_type: arxiv_paper
---

# Multi-turn QA Data from Human Demonstrations

**Multi-turn QA Data from Human Demonstrations** is a dataset format where sequences of human demonstration trajectories are converted into structured, multi-turn question-answering pairs. This data is specifically designed to fine-tune Vision-Language Models ([[VLM]] ⚠️ ⚠️) for navigation reasoning tasks, enabling them to perform compositional, hierarchical decision-making in embodied environments.

## Parameters

| Parameter | Value |
|-----------|-------|
| Source | [[Human Demonstration Trajectories]] ⚠️ ⚠️ |
| Format | Multi-turn question-answering pairs |
| Purpose | Fine-tune VLM for navigation reasoning |

Each human demonstration trajectory is segmented into a logical sequence of questions and answers that capture the underlying reasoning process. This transforms raw teleoperation data into a supervised learning signal that teaches the VLM both *what* actions to take and *why*.

## Capabilities

- **Enables structured reasoning in VLM**: By presenting reasoning chains as multi-turn QA, the model learns to decompose a high-level navigation goal into intermediate steps, mimicking the human demonstrator's decision process.
- **Provides compositional knowledge for hierarchical decision-making**: The QA pairs naturally embed sub‑task decomposition, allowing the model to handle complex instructions that require planning, obstacle avoidance, and context‑aware action selection.

## Relationships

- **Used in**: This data construction method is a core component of [[CL-CoTNav]], which employs multi-turn QA derived from human demonstrations to fine‑tune a VLM for Chain‑of‑Thought (CoT) navigation in indoor environments.
- **Depends on**: [[Human Demonstration Trajectories]] ⚠️ ⚠️ as the raw input; [[VLM]] ⚠️ ⚠️ as the target model to be fine‑tuned.

The multi-turn QA data serves as a bridge between unstructured human behavior and structured model reasoning, enabling the VLM to learn interpretable and generalizable navigation policies.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Multi-turn QA Data from Human Demonstrations` --[[related_to]] ⚠️--> `CL-CoTNav` _(wikilink)_
