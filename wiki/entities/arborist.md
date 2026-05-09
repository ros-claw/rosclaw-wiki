---
id: arborist
title: Arborist
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T03:53:32'
last_reinforced: '2026-04-30T03:53:32'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

# Arborist

**Arborist** is an [[LLM]] ⚠️-based module designed for autonomous plan adjustment in robotic task execution. It enables re-planning without human intervention by reasoning over task failures and generating revised action sequences.

## Capabilities

- **Autonomous plan adjustment**: Arborist can detect when an original plan fails (e.g., due to a grasped object slipping, sensor error, or environment change) and synthesize a new sub-plan on the fly. This is critical for long-horizon manipulation tasks where perfect initial plans are unrealistic.

## Role in Adaptive Replanning

Arborist functions as a core component within an [[Adaptive Replanning]] framework. It receives feedback from execution monitors and uses [[Prompt Engineering]] ⚠️ or [[In-Context Learning]] ⚠️ to produce updated task sequences. Its decisions may be conditioned on [[Task and Motion Planning]] ⚠️ (TAMP) primitives or low-level [[Controller]] ⚠️ interfaces.

## Relationship to Other Entities

- **depends_on**: [[Large Language Model]] (LLM) as its underlying reasoning engine.
- **implements**: [[Autonomous Replanning]] ⚠️ (a skill or algorithm for adapting to execution failures).
- **part_of**: [[Adaptive Replanning]] (a broader framework or algorithm class).
- **related_to**: [[Failure Recovery]] ⚠️ — Arborist’s replanning can be seen as a form of online failure recovery.

## Source

This definition is derived from *arxiv paper 2503.22942* (see [[Sources: Adaptive Replanning via LLMs]] ⚠️).