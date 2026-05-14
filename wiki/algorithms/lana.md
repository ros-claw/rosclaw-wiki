---
id: lana
title: LANA
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:12:19'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2303.08409.pdf
source_type: arxiv_paper
---

## LANA (Language-Aligned Navigation Agent)

**LANA** is a unified neural architecture for **visual-language navigation** (VLN) that jointly learns to follow natural language instructions and to generate route descriptions. Unlike prior task-specific agents, LANA employs a shared encoder representation and two decoders, enabling bidirectional communication between humans and robots.

LANA is introduced in the paper *"LANA: A Language-Capable Navigator for Instruction Following and Generation"* (arXiv:2303.08409).

### Abstract

> LANA is a language-capable navigation agent that simultaneously learns instruction following and generation with a single model.

This unified design allows the same architecture to both execute human-written navigation commands and produce natural-language route descriptions, effectively doubling the agent's communicative utility without requiring separate pipelines.

### Summary

LANA uses two encoders (one for routes, one for language) that are shared by two decoders: one for **action prediction** (instruction following) and one for **instruction generation** (producing route descriptions). The model is trained jointly on both objectives using a pretrain‑then‑fine‑tune paradigm, achieving performance comparable to—and at approximately half the complexity of—many recent task‑specific VLN solutions. By exploiting cross-task knowledge, LANA learns representations that benefit both directions of human-robot interaction.

### Capabilities

- Execute human-written navigation commands in unseen environments.
- Provide natural-language route descriptions to human users.
- Explain its own navigation behaviors (e.g., why a certain path was chosen).
- Assist human wayfinding by generating turn-by-turn or summary directions.

### Parameters

| Parameter | Value |
|-----------|-------|
| Model structure | Two encoders (route + language) shared by two decoders (action prediction, instruction generation) |
| Optimization objectives | Instruction following + instruction generation |
| Training paradigm | Pretraining + fine‑tuning |
| Complexity | Approximately half the parameters of recent task‑specific VLN agents (nearly half of task‑specific solutions) |

### Relationships

- **Uses:**
    - Encoder-decoder architecture ⚠️ — LANA’s core architecture relies on shared encoders and separate decoders for the two tasks.
    - Cross-task knowledge ⚠️ — Joint training allows the agent to leverage shared representations between instruction following and generation.
- **Depends on:**
    - Visual-Language Navigation (VLN) ⚠️ — LANA is an algorithm designed for the VLN task, operating on visual input and natural language commands.
    - Pretraining and fine-tuning ⚠️ — The model follows a two-stage training paradigm where large-scale pretraining is followed by task-specific fine-tuning.
- **Supersedes:**
    - Task‑specific VLN agents that only perform instruction following, by adding instruction generation capability without a separate generation pipeline.

### References

- **source:** `data/raw/papers/2303.08409.pdf`
- **arXiv:** [2303.08409](https://arxiv.org/abs/2303.08409)