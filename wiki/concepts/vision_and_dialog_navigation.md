---
id: vision_and_dialog_navigation
title: Vision-and-Dialog Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:44:35'
last_reinforced: '2026-04-30T02:44:35'
supersedes: []
sources:
- papers/2002.10638.pdf
source_type: arxiv_paper
---

# Vision-and-Dialog Navigation

## Overview

**Vision-and-Dialog Navigation** is an extension of [[Vision-Language Navigation (VLN)]] in which an agent navigates through an environment by interacting via **dialog** — a history of questions and answers — in addition to visual and language instructions. Unlike standard VLN, which provides a single natural language instruction at the start, this task requires the agent to actively engage in conversation, asking clarification questions and receiving answers, thereby combining visual perception, language grounding, and dialog state tracking.

This task is part of a broader class of [[VLN tasks]] ⚠️ and is significantly improved by [[Prevalent pre-training]] ⚠️, which provides generic representations that boost performance on the more demanding dialog-conditioned navigation.

## Capabilities

- Requires understanding of **dialog context** in addition to visual and language inputs.
- Agent must integrate information from multiple turns of conversation while maintaining a coherent belief about the environment and goal.

## Relation to VLN

Vision-and-dialog navigation **extends** the standard [[Vision-Language Navigation (VLN)]] paradigm by adding a **conversational component**. While VLN agents follow a static instruction, vision-and-dialog agents must track a dynamic sequence of queries and responses, making the task more challenging. Prevalent’s generic representations, which are pre-trained on large-scale vision-and-language data, have been shown to boost performance significantly on this task by providing robust cross-modal embeddings that generalize well to dialog flows.

> **Source:** [arXiv:2002.10638] — *Prevalent: Pre-training for Vision-and-Dialog Navigation*