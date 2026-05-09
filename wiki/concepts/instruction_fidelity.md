---
id: instruction_fidelity
title: Instruction Fidelity
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:07:49'
last_reinforced: '2026-04-30T03:07:49'
supersedes: []
sources:
- papers/1905.12255.pdf
source_type: arxiv_paper
---

# Instruction Fidelity

**Instruction fidelity** is a concept in embodied AI and vision-and-language navigation (VLN) that measures the degree to which an agent's navigational path follows the sequence of actions described in natural language instructions, as opposed to merely reaching the final goal. It shifts evaluation focus from outcome-based success (e.g., reaching the target location) to process-based alignment with the instruction.

## Definition

> Instruction fidelity refers to the degree to which an agent's navigational path follows the sequence of actions described in natural language instructions, as opposed to merely reaching the final goal.

## Capabilities

- Focuses on whether the agent's sequence of actions corresponds to the instructions, not just goal completion.
- Provides a more fine-grained evaluation of instruction following, penalizing deviations or shortcuts that achieve the goal but violate the intended route.

## Usage in Evaluation

Instruction fidelity is a core motivation behind metrics like [[CLS metric]] ⚠️ ⚠️ (Coverage-weighted by Language Similarity) and is explicitly considered in the [[R4R dataset]] ⚠️ ⚠️ (Room-to-Room). These resources evaluate agents not only on final destination accuracy but on how closely their path matches the linguistic description.

## Relation to Other Concepts

- Used by [[CLS metric]] ⚠️ ⚠️ – the CLS metric incorporates instruction fidelity by penalizing path deviations from the instruction.
- Used by [[R4R dataset]] ⚠️ ⚠️ – the R4R dataset includes trajectory-instruction pairs that require strict adherence to the described route.
- Contrasts with [[Goal Completion]] ⚠️ metrics that only consider whether the agent arrived at the correct location.