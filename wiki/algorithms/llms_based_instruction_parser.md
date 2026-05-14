---
id: llms_based_instruction_parser
title: LLMs-based instruction parser
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:08:06'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

## Overview

The **LLMs-based instruction parser** is an algorithm component that leverages pre-trained large language models (LLMs) to translate free-form natural language instructions into structured, executable macro-action sequences. It serves as the language understanding backbone for embodied agents, bridging high‑level task descriptions and low‑level control.

## Parameters

- **Input**: natural language instruction (free-form text)
- **Output**: sequence of macro-action descriptions (e.g., "go to the door", "turn left")
- **Base model**: Large language model (LLM) – the parser relies on the broad semantic and syntactic knowledge captured by pre‑trained LLMs.

## Capabilities

- Converts free-form language into structured macro-actions, enabling the agent to interpret diverse linguistic commands.
- Extracts waypoint-level goals from instructions, providing intermediate spatial targets that guide navigation.

## Relationships

- **Depends on**: Foundation models – the parser uses a pre‑trained LLM for language understanding.
- **Part of**: Vision and Language Navigation in the Real World via Online Visual Language Mapping ⚠️ – this parser is integrated into a real‑world VLN system that combines visual, linguistic, and metric mapping.
- **Used by**: Proposed VLN framework ⚠️ – previously noted as the high-level system using this parser; the same framework corresponds to the paper cited above.

## Instruction Parsing

This component leverages pre-trained LLMs to map natural language commands to a sequence of high-level macro-actions, enabling flexible instruction understanding. By decomposing a user’s request into ordered macro‑actions (e.g., “go to the kitchen”, “grab the cup”), the parser produces an action plan that can be executed by downstream controllers. Additionally, the parser extracts **waypoint-level goals** (e.g., specific sub‑goals like “the doorway” or “the table”) to guide the agent through complex environments step by step. The use of LLMs allows the system to handle ambiguous phrasing, synonyms, and complex task compositions without hand‑crafted templates.