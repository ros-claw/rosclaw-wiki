---
id: passive_navigation
title: Passive navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:19:49'
last_reinforced: '2026-04-30T03:19:49'
supersedes: []
sources:
- papers/2108.11544.pdf
source_type: arxiv_paper
---

# Passive Navigation

**Passive navigation** is a subtype of [[Multi-turn navigation]] in which the agent is not allowed to question the instruction. The agent must follow the provided turn-by-turn commands without requesting clarification, reprompting, or seeking additional information during the traversal.

This contrasts with **active navigation** (or interactive navigation), where the agent can ask for disambiguation or query the environment to resolve ambiguity. In passive navigation, all instructions are assumed to be complete and sufficient at the outset, placing a greater burden on the agent to interpret and execute them correctly.

## Relationship to Multi‑turn Navigation

- **subtype_of** [[Multi-turn navigation]] – passive navigation inherits the multi-turn (stepwise) structure of its parent category but restricts the interaction modality.

## Key Characteristics

- One-way communication: the instruction source provides the entire path description without feedback loops.
- The agent must rely solely on its internal knowledge, sensor data, and the predetermined instruction.
- Often used in benchmark tasks where reproducibility and standardized evaluation are required (e.g., R2R, Room‑to‑Room tasks).

## Limitations

- Ambiguous or under‑specified instructions can lead to failure without any opportunity to recover or ask for clarification.
- Real‑world deployment typically benefits from **active** or **interactive** approaches, but passive navigation remains a useful simplification for controlled experimentation.