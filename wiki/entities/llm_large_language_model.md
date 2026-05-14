---
id: llm_large_language_model
title: LLM (Large Language Model)
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:57'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# LLM (Large Language Model)

A **Large Language Model (LLM)** is a neural network trained on vast text corpora, capable of understanding and generating human-like language. In robotics and embodied AI, LLMs are leveraged for **high-level reasoning and decision-making** — bridging natural language instructions with actionable commands. The LLM operates in a **zero-shot** manner, meaning it can perform these tasks without task-specific fine-tuning, relying solely on its pre‑training.

## Capabilities

As reported by the AO-Planner and PathAgent systems (source: arxiv paper 2407.05890), an LLM is used to:

- **Select candidate waypoints** – from a set of reachable poses or regions, the LLM identifies those most relevant to the task, based on affordances and environmental context.
- **Reason about a path** – it evaluates sequences of waypoints, considering feasibility, efficiency, and natural language constraints.
- **Select candidate waypoints based on affordances** – an extension of the above, emphasizing the LLM’s ability to ground linguistic concepts in physical possibilities.
- **Reason over environmental information** – integrating perceptual data (e.g., obstacle locations, terrain types) into its planning process.

These capabilities allow an LLM to function as a *semantic planner*: converting abstract goals (e.g., “move behind the obstacle”) into concrete navigation targets.

## Usage

The LLM is a core component of both AO-Planner and PathAgent, each of which depends on its waypoint selection and path reasoning to produce executable motion commands.

- AO-Planner **uses** LLM ⚠️ ⚠️ – the planner invokes the LLM to ground language in spatial reasoning.
- PathAgent **uses** LLM ⚠️ ⚠️ – the agent relies on the LLM for high-level decision‑making during path generation.

No other relationships are documented in the current source.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `LLM (Large Language Model)` --uses ⚠️ ⚠️--> `AO-Planner`
- `LLM (Large Language Model)` --uses ⚠️ ⚠️--> `PathAgent`