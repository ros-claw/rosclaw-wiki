---
id: vln_trans
title: VLN-Trans
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:13:22'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

# VLN-Trans

## Overview

VLN-Trans is a translator module designed for [[Vision and Language Navigation]] (VLN) agents. It addresses two instruction issues: **unrecognizable landmarks** due to differing vision abilities between humans and agents, and **non-distinctive landmarks** that could apply to multiple targets. The module converts complex navigation instructions into stepwise **sub-instruction representations** that emphasize landmarks that are both recognizable and distinctive given the agent’s visual capabilities and current viewpoint.

The module acts as a bridge between raw human language and actionable agent plans, enabling the agent to focus on [[distinctive landmarks]] that are visible from its perspective rather than relying on ambiguous descriptions.

## Capabilities

- Converts original navigation instructions into easy-to-follow sub-instruction representations at each step.
- Focuses on recognizable and distinctive landmarks based on the agent’s visual abilities and observed environment.

These capabilities are learned jointly with the navigation agent using a synthetic sub-instruction dataset.

## Methodology

The translator module is trained jointly with the navigation agent using a newly constructed synthetic dataset of sub-instructions. The sub-instruction representation is learned to decompose long, complex routes into shorter segments, each aligned with a visible landmark. The training process explicitly accounts for the agent’s [[Navigation Agent Visual Abilities]] ⚠️ ⚠️, ensuring that the generated sub-instructions refer to landmarks the agent can perceive and distinguish.

## Training Data

To support joint training of the translator and the navigation agent, a new **synthetic sub‑instruction dataset** was created. This dataset pairs original instructions with stepwise sub-instructions that highlight landmarks salient to the agent’s view. The dataset is used in conjunction with standard VLN benchmarks.

- **Uses**: [[R2R dataset]], [[R4R dataset]] ⚠️ ⚠️, [[R2R-Last dataset]], [[Synthetic Sub-Instruction Dataset]]
- **Depends on**: [[sub-instruction representation]], [[Navigation Agent Visual Abilities]] ⚠️ ⚠️

## Relationships

VLN‑Trans is a core component of a complete [[Vision and Language Navigation System]] ⚠️, where it acts as the front‑end translator that bridges language input and agent action.

## Evaluation

VLN-Trans achieves **state-of-the-art results** on the following benchmarks:

- [[R2R dataset]]
- [[R4R dataset]] ⚠️ ⚠️
- [[R2R-Last dataset]]

It demonstrates significant improvements in task completion rates and navigation efficiency compared to prior methods, particularly on instructions that contain ambiguous or landmark-poor language.

## Source

- Paper: `data/raw/papers/2302.09230.pdf`