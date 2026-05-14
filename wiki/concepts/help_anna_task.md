---
id: help_anna_task
title: Help, Anna! Task
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:45:20'
last_reinforced: '2026-04-30T02:45:20'
supersedes: []
sources:
- papers/2002.10638.pdf
source_type: arxiv_paper
---

# Help, Anna! Task

## Overview

The **Help, Anna! Task** is a Vision-and-Language Navigation (VLN) benchmark where an agent must follow natural language instructions to help a person named Anna, often involving object manipulation or interaction in a visual environment. This task extends standard VLN by incorporating an interactive social component, requiring the agent to understand both spatial navigation and task-oriented language.

## Capabilities

- The agent must follow natural language instructions in a visual environment, interpreting commands like "go to the kitchen and hand Anna the apple."
- The task demands grounding of instructions to specific objects and locations, as well as the ability to execute physical interactions (e.g., grasping, handing).

## Relationships

- **Part of VLN tasks ⚠️** — The Help, Anna! Task is a specific instance of VLN, adding an interactive, human-in-the-loop element.
- **Improved by Prevalent Pre-training ⚠️** — Prevalent, a pre-training method for VLN, demonstrates transferability by achieving state-of-the-art results on this task, validating the effectiveness of its representation learning approach.

## Source

- ArXiv paper: [2002.10638] — "Prevalent: A Pre-training Method for Vision-and-Language Navigation" (describes transfer of Prevalent to the Help, Anna! benchmark).