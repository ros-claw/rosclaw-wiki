---
id: decoupling_training
title: decoupling training
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:25:39'
last_reinforced: '2026-04-30T00:25:39'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# Decoupling Training

**Decoupling Training** is a training methodology that separates the learning of System 1 (high-level reasoning) and System 2 (low-level control) to preserve the generalization capabilities of a Vision-Language Model (VLM) while enabling efficient learning of local navigation behaviors.

## Overview

In the context of [[Visual Language Navigation]] ⚠️ (VLN), end-to-end training of a VLM together with a navigation policy often leads to catastrophic forgetting of the VLM's broad semantic knowledge. Decoupling training addresses this by treating the two systems independently: System 1 (typically a [[Vision-Language Model]]) can be frozen or fine-tuned separately on high-level tasks, while System 2 (the local navigation policy) is trained using reinforcement learning or imitation learning on environment-specific interactions. This separation allows the VLM to retain its generalization across diverse scenes while the navigation policy adapts to fine-grained local motion requirements.

## Definition

> Training System 1 and System 2 separately to preserve VLM generalization while enabling efficient local navigation learning.

## Applications

This concept is employed by the [[DualVLN]] framework, which instantiates decoupling training as a core design principle to combine semantic understanding with reactive navigation.

## Relationship Annotations

- **used_by**: [[DualVLN]]
- **depends_on**: [[Vision-Language Model]], [[Navigation Policy]] ⚠️
- **contrasts_with**: [[End-to-End Training]] ⚠️

## Source

- arxiv paper: `papers/2512.08186.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `decoupling training` --[[related_to]] ⚠️--> `DualVLN` _(wikilink)_
