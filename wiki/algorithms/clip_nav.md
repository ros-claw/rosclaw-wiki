---
id: clip_nav
title: CLIP-Nav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:07:51'
last_reinforced: '2026-04-30T02:07:51'
supersedes: []
sources:
- papers/2211.16649.pdf
source_type: arxiv_paper
---

# CLIP-Nav

**CLIP-Nav** is a zero-shot algorithm for [[vision-and-language navigation]] (VLN) that uses the [[CLIP]] model to make sequential navigational decisions from natural language referring expressions, without requiring any dataset-specific finetuning.

## Capabilities

- **Zero-shot VLN**: Operates directly on natural language instructions and visual observations without task-specific training.
- **Sequential decision-making**: Leverages CLIP’s joint image–text embedding space to compare the current view against the goal description at each step.
- **No finetuning**: Avoids the need for large-scale navigation datasets and supervised adaptation.

## Method

CLIP-Nav formulates navigation as a series of similarity comparisons. At each timestep, it encodes the current camera frame and a set of candidate directions (or panoramas) using CLIP’s visual encoder. The referring expression is encoded with CLIP’s text encoder. The agent selects the direction whose visual embedding is most similar to the text embedding of the instruction. This process is repeated until the goal is reached or a termination criterion is met.

## Evaluation

CLIP-Nav was evaluated on the **REVERIE** benchmark. Performance metrics include:

- **SR** (Success Rate)
- **SPL** (Success weighted by Path Length)
- **RCS** (Relative Change Score)

These metrics demonstrate competitive results compared to a [[supervised baseline]] ⚠️ ⚠️, despite using no training data or fine-tuning.

## Relationships

- **Uses**: [[CLIP]] – the core vision–language model for cross-modal matching.
- **Compared to**: [[supervised baseline]] ⚠️ ⚠️ – a typical trained navigation policy used as a reference point for zero-shot performance.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CLIP-Nav` --[[based_on]] ⚠️--> `vision-and-language navigation`
- `CLIP-Nav` --[[extends]] ⚠️--> `CLIP`
