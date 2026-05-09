---
id: cooperative_localization
title: Cooperative Localization
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:59:57'
last_reinforced: '2026-04-30T02:59:57'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

# Cooperative Localization

**Cooperative Localization** is a task from the [[Where Are You? (WAY) Dataset]] ⚠️ ⚠️ ⚠️ ⚠️ that models collaborative spatial reasoning between two agents — an **Observer** and an **Locator** — who must complete a localization objective entirely through dialog. Unlike single-agent localization benchmarks, this task captures the full interactive loop of question‑asking, description, and grounding.

## Task

The goal of Cooperative Localization is to simulate a **full cooperative localization dialog**. The Observer holds knowledge of the target location (e.g., coordinates or landmark) and must guide the Locator to that location using natural language. The Locator must interpret the Observer’s utterances, ask clarifying questions when needed, and converge on the correct position. The task requires:

- **Spatial reasoning** — mapping language to coordinates or scene regions.
- **Dialog state tracking** — maintaining shared context across turns.
- **Mutual grounding** — reaching common understanding incrementally.

This task is a key component of the [[Where Are You? (WAY) Dataset]] ⚠️ ⚠️ ⚠️ ⚠️, where examples are annotated with full dialog histories and final successful localizations.

## Capabilities

A model trained on Cooperative Localization can:

- **Simulate complete cooperative localization dialogs** from scratch (both agent roles).
- Generate and understand spatial references in a shared environment.
- Resolve ambiguity through multi-turn clarification.

## Relationships

- **Part of**: [[Where Are You? (WAY) Dataset]] ⚠️ ⚠️ ⚠️ ⚠️ – Cooperative Localization is one of the core tasks defined in the WAY dataset.
- **Depends on**: [[Where Are You? (WAY) Dataset]] ⚠️ ⚠️ ⚠️ ⚠️ – the task relies on the dialog‑grounding annotations and spatial scenarios provided by the dataset.
- **Implements**: [[Embodied Dialog]] ⚠️ – cooperative localization is a concrete instantiation of embodied dialog where both agents operate in a real or simulated space.
- **Contrasts with**: [[Single-Agent Localization]] ⚠️ – where one agent independently determines its position; Cooperative Localization requires joint reasoning through dialog.

## See Also

- [[Spatial Language Grounding]] ⚠️
- [[Multi‑Agent Systems]] ⚠️