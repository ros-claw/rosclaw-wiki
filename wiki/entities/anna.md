---
id: anna
title: ANNA
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:24:25'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1909.01871.pdf
source_type: arxiv_paper
---

# ANNA

**ANNA (Automatic Natural Navigation Assistant)** is a simulated human assistant within the [[HANNA]] framework. It provides multimodal guidance—using both natural language and visual cues—to direct an agent toward its object goals.

## Description

ANNAs are simulated assistants that operate inside HANNA to provide multimodal help to agents. They are triggered upon agent request and output navigation directions using a combination of spoken language and visual indicators (e.g., pointing or highlighting paths).

## Capabilities

- Provides navigation directions using natural language and visual cues
- Guides agent towards object goals
- Upon request, gives multimodal instructions that combine speech and visual hints

## Role

ANNA acts as an interactive aid, reducing the agent's reliance on internal navigation models by providing external guidance. The assistant is invoked when the agent explicitly requests help, making the navigation process more robust in unfamiliar or complex environments.

## Relationships

- **Part of**: ANNA is a component of the [[HANNA]] system.
- **Used by**: The [[HANNA]] agent requests guidance from ANNA.
- **Assists**: ANNA supports agent navigation through its multimodal output.

### Correction to automatic links
The earlier automatic link `ANNA --[[depends_on]] ⚠️--> HANNA` was reversed: ANNA is actually a sub‑module of HANNA, not a dependency. The correct relation is `part_of`.