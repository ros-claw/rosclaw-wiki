---
id: exploration_verification_strategy
title: Exploration-Verification strategy
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:36:40'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2601.04699.pdf
source_type: arxiv_paper
---

# Exploration-Verification Strategy

The **Exploration-Verification strategy** is a two-phase algorithm for trajectory correction that leverages the structured nature of logical instructions. It decomposes correction into an *exploration phase* and a *verification phase*, enabling robust recovery from execution errors without requiring full replanning. In the context of [[SeqWalker]], it functions as a core component of the [[Low-Level Planner]] to verify and correct navigation errors.

## Summary
A strategy used in the Low-Level Planner of SeqWalker to verify and correct navigation errors.

## Phases

The strategy operates as follows:

1. **Exploration Phase**  
   The system attempts multiple corrective actions by perturbing the current trajectory within a bounded action space. This phase generates candidate trajectories that might satisfy the intended instruction.

2. **Verification Phase**  
   Each candidate trajectory is checked against the logical instruction constraints. Only those that meet the structural requirements (e.g., preconditions, ordering, state invariants) are accepted. The verified trajectory is then executed.

This separation allows the [[Low-Level Planner]] to efficiently search for corrections while ensuring that any accepted path respects the high-level goal structure.

## Capabilities

- **Trajectory error correction using logical instruction structure** – By exploiting the inherent logic in task instructions, the strategy narrows the search space for corrections and improves success rate over naive replanning.
- **Instruction-guided verification** – Leverages the logical structure of instructions to detect and correct navigation errors (reinforced by paper `papers/2601.04699.pdf`).

## Relationships

- **part_of**: [[Low-Level Planner]] – The strategy is a component of the Low-Level Planner, which itself is part of [[SeqWalker]].
- **used_by**: [[SeqWalker]] – SeqWalker invokes the Low-Level Planner, which relies on this strategy for trajectory correction.
- **part_of (indirect)**: [[SeqWalker]] – Through the Low-Level Planner’s role in the larger system.

> **Note**: Previous descriptions listed the strategy as *used_by* the Low-Level Planner. The paper `papers/2601.04699.pdf` clarifies that it is a part of the Low-Level Planner itself.

## See Also

- [[Trajectory Correction]] ⚠️
- [[Logical Instruction Parsing]] ⚠️
- [[Hierarchical Task Execution]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Exploration-Verification strategy` --[[extends]] ⚠️ ⚠️--> `Low-Level Planner`
- `Exploration-Verification strategy` --[[extends]] ⚠️ ⚠️--> `SeqWalker`