---
id: r2r_last_dataset
title: R2R-Last dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:39:32'
last_reinforced: '2026-04-30T01:39:32'
supersedes: []
sources:
- papers/2302.06072.pdf
source_type: arxiv_paper
---

# R2R-Last Dataset

The **R2R-Last** dataset is a specialized benchmark within the [[Room-to-Room (R2R)]] family, designed to evaluate Vision-and-Language Navigation (VLN) agents on the **last action** prediction task. Unlike the standard R2R dataset which requires full path instruction following, R2R-Last isolates the final step of a navigation episode, testing an agent's ability to correctly identify the terminating action (typically a `stop` or final direction) based on the full preceding trajectory and instruction.

## Overview

R2R-Last is used to assess **actional atomic-concept learning** – the capacity of a model to learn fine-grained grounding between language tokens and discrete navigational commands. It is particularly valuable for diagnosing whether a VLN agent truly understands the semantics of navigation instructions versus simply pattern-matching action sequences.

The benchmark splits existing R2R trajectories into a prefix (all steps except the last) and the final action. The agent must predict the last action given the visual observations and language instruction up to that point. This challenges models to focus on critical linguistic cues that indicate termination or final orientation.

## Capabilities

- **Used to evaluate state-of-the-art in VLN**: R2R-Last serves as a diagnostic benchmark for evaluating progress in embodied instruction following. It isolates a core subproblem – action grounding – from the larger sequence prediction task.

## Relationships

- `evaluates` → [[Actional Atomic-Concept Learning (AACL)]]: The R2R-Last benchmark is specifically employed in the AACL framework to test whether learned atomic concepts (e.g., "turn left", "stop") are correctly aligned with visual observations.

## See Also

- [[Room-to-Room (R2R) Dataset]]
- [[Vision-and-Language Navigation (VLN)]] ⚠️
- [[Actional Atomic-Concept Learning (AACL)]]

## References

- *Actional Atomic-Concept Learning for Vision-and-Language Navigation* (arXiv:2302.06072) – Introduces the R2R-Last benchmark and AACL method.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `R2R-Last dataset` --[[applies_to]] ⚠️--> `Room-to-Room (R2R) Dataset`
**Pending review:**
- `R2R-Last dataset` --[[related_to]] ⚠️--> `Actional Atomic-Concept Learning (AACL)` _(wikilink)_
