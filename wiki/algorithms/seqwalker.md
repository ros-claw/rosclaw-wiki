---
id: seqwalker
title: SeqWalker
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:36:08'
last_reinforced: '2026-04-29T20:36:08'
supersedes: []
sources:
- papers/2601.04699.pdf
source_type: arxiv_paper
---

## SeqWalker

**SeqWalker** is a hierarchical planning navigation model designed for **Sequential-Horizon Vision-and-Language Navigation (VLN)**. It addresses the challenge of **information overload** in long-horizon VLN tasks by dynamically breaking complex, multi-step language instructions into contextually relevant sub-instructions based on real-time visual observations.

---

### Overview

SeqWalker operates on a two-tier [[Hierarchical Planning]] architecture:

- **[[High-Level Planner]]**: Extracts global instruction segments and decomposes them into sub-goals using visual grounding. It decides *which* part of the instruction to follow next based on the current scene.
- **[[Low-Level Planner]]**: Executes the selected sub-instruction by generating discrete actions (e.g., move forward, turn, interact) while continuously verifying progress against the sub-goal.

The model employs an **[[Exploration–Verification strategy]] ⚠️ ⚠️** to detect and correct trajectory errors. If the agent deviates from the intended path or encounters an ambiguous situation, it triggers a verification loop that re-evaluates the sub-instruction or falls back to exploration.

---

### Capabilities

- **Sequential multi-task execution**: Navigates environments using complex, long-horizon language instructions that specify multiple tasks (e.g., "go to the kitchen, grab the apple, then bring it to the dining table").
- **Dynamic sub-instruction selection**: Chooses the next relevant sub-instruction based on [[visual observations]] ⚠️ ⚠️ and [[language instructions]] ⚠️ ⚠️, reducing cognitive load.
- **Error recovery**: Uses the Exploration–Verification strategy to backtrack, re-plan, or re-explore when trajectory mismatches are detected.

---

### Key Relationships

| Relationship | Entity | Description |
|--------------|--------|-------------|
| **uses** | [[Hierarchical Planning]] | Decomposes navigation into high-level and low-level planners. |
| **uses** | [[High-Level Planner]] | Selects sub-goals from the global instruction. |
| **uses** | [[Low-Level Planner]] | Executes sub-goals into actions. |
| **uses** | [[Exploration–Verification strategy]] ⚠️ ⚠️ | Detects and corrects errors during navigation. |
| **depends on** | [[visual observations]] ⚠️ ⚠️ | Scene perception from egocentric camera feed. |
| **depends on** | [[language instructions]] ⚠️ ⚠️ | Complex, long-horizon textual commands. |
| **addresses** | [[information overload]] ⚠️ in VLN | Prevents the agent from being overwhelmed by lengthy instructions. |

---

### Source

The SeqWalker architecture is described in the following preprint:

> *SeqWalker: Sequential-Horizon Vision-and-Language Navigation*  
> arXiv:2601.04699 (2025)

---
*This page is part of the [[ROSClaw Knowledge Base]] ⚠️.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SeqWalker` --[[extends]] ⚠️ ⚠️--> `High-Level Planner`
- `SeqWalker` --[[extends]] ⚠️ ⚠️--> `Low-Level Planner`
