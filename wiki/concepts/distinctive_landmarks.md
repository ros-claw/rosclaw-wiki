---
id: distinctive_landmarks
title: Distinctive Landmarks
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:03:21'
last_reinforced: '2026-04-30T02:03:21'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

# Distinctive Landmarks

Distinctive Landmarks are visual or spatial reference points that are **unique enough to distinguish a single target among multiple candidate viewpoints**, as opposed to landmarks that apply to several targets. This concept is fundamental to Instruction Disambiguation in VLN ⚠️ ⚠️ ⚠️ (Vision-and-Language Navigation), where the agent must resolve ambiguous natural language instructions by identifying which landmark uniquely specifies the intended goal.

## Properties

- **Uniqueness**: A distinctive landmark can be described by features that appear only at the target location, enabling the agent to eliminate other candidates.
- **Context Dependence**: The distinctiveness of a landmark depends on the set of possible viewpoints – a landmark may be distinctive in one environment but not in another.
- **Relation to Salience**: While salience measures visual prominence, distinctiveness is about discriminative power relative to competing landmarks.

## Relationship to Instruction Disambiguation

Distinctive Landmarks are a **part of** Instruction Disambiguation in VLN ⚠️ ⚠️ ⚠️. In tasks where multiple candidate targets match a spoken or written instruction, the system must leverage distinctive descriptions to narrow down to the correct location. This concept directly supports the disambiguation process by providing a criterion for evaluating which landmarks are most useful for resolving ambiguity.

## Contradiction with Non-Distinctive Landmarks

Distinctive Landmarks **contradict** Non-Distinctive Landmarks ⚠️ ⚠️. Where distinctive landmarks uniquely identify a single target, non-distinctive landmarks are those that could refer to several candidates (e.g., "the red door" when multiple doors are red). Understanding this contrast is essential for designing robust navigation agents that can handle ambiguous language.

## Usage in Research

In Vision-and-Language Navigation (VLN) ⚠️ models, distinctive landmarks are often extracted from panoramic views and compared against candidate target images using learned similarity metrics. The degree of distinctiveness can be computed as the inverse of the number of times a landmark description matches across different viewpoints.

---

*See also: Instruction Disambiguation in VLN ⚠️ ⚠️ ⚠️, Non-Distinctive Landmarks ⚠️ ⚠️, Salient Landmarks ⚠️*