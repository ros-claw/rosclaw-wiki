---
id: large_language_models
title: Large Language Models
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:10:14'
last_reinforced: '2026-04-30T04:10:14'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

# Large Language Models

**Large Language Models (LLMs)** are deep neural network models trained on vast text corpora to generate human-like text and perform complex language understanding tasks. In the context of embodied intelligence and robotic systems, they serve as high-level reasoning components that translate natural language instructions into executable action sequences.

## Overview

LLMs provide a powerful interface between natural language and robotic control. By leveraging their reasoning and generation capabilities, robots can interpret ambiguous human commands, decompose them into sub-tasks, and adapt their plans in real-time based on environmental feedback. This makes them integral to modern task planning and adaptive replanning systems.

## Capabilities

- **Task planning via primitive skill tree:** The LLM decomposes a high-level goal into a sequence of atomic skills drawn from a Primitive Skill Tree.
- **Adaptive replanning via Advisor and Arborist modules:** When the initial plan fails or new information arrives, the LLM leverages the Advisor module to assess alternatives and the Arborist module to restructure the plan, enabling dynamic re-planning.

## Relationships

- **Used by:** AINav — the navigation framework that employs the LLM for both initial task planning and adaptive replanning.
- **Used by:** Primitive Skill Tree — the LLM selects and orders skills from this tree.
- **Used by:** Adaptive Replanning — the LLM powers the Advisor and Arborist modules within this process.

## Related Concepts

- Large Language Models are a class of Foundation Models.
- Their integration with ROS2 enables natural language command interfaces in robotic systems.
- For task planning, they often rely on Symbolic Planners ⚠️ to ground abstract actions.