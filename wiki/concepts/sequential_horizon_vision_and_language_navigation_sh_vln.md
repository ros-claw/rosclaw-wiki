---
id: sequential_horizon_vision_and_language_navigation_sh_vln
title: Sequential-Horizon Vision-and-Language Navigation (SH-VLN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:57:52'
last_reinforced: '2026-04-29T23:57:52'
supersedes: []
sources:
- papers/2601.04699.pdf
source_type: arxiv_paper
---

# Sequential-Horizon Vision-and-Language Navigation (SH-VLN)

**SH-VLN** (Sequential-Horizon Vision-and-Language Navigation) is a challenging variant of [[Vision-and-Language Navigation (VLN)]] ⚠️ in which an agent must execute **multiple sequential navigation tasks** guided by complex, long-horizon language instructions. The multi-task nature and extended instruction length lead to **information overload** and significant **performance degradation** in standard VLN models.

## Overview

Traditional VLN involves a single instruction and a single goal. SH-VLN instead requires the agent to handle a **sequence of sub-instructions** that together form a long-horizon goal. For example, an agent might be asked: *"Go to the kitchen, pick up the apple, then bring it to the dining table, and finally return to the living room."* Each sub-task must be completed **sequentially** without resetting the environment or receiving new observations between steps.

## Capabilities

- Presents a **challenging scenario** where agents must sequentially execute multi-task navigation with long-horizon instructions.
- Tests the **memory, planning, and instruction-following** abilities of VLN agents under cumulative cognitive load.
- Reveals **limitations** of current models, which often fail when required to maintain state across multiple sub-goals.

## Relationship to Standard VLN

SH-VLN **supersedes** [[Standard VLN]] ⚠️ by introducing greater complexity:

| Aspect | Standard VLN | SH-VLN |
|--------|--------------|--------|
| Instruction | Single, short horizon | Multiple, long horizon sequences |
| Tasks | One goal | Multiple sequential sub-tasks |
| Memory | Minimal working memory required | Must track progress across sub-goals |
| Typical models | Successfully execute short commands | Degrade due to information overload |

## Challenges

- **Information overload**: Long instructions exceed typical attention windows.
- **Sequential memory**: Agents must remember past actions and current intent.
- **Multi-task coordination**: RL or imitation learning paradigms struggle with multiple sub-goals.
- **Evaluation**: New metrics are needed to track sub-task completion and sequence correctness.

## See Also

- [[Embodied AI]] — broader field of intelligence in physical agents.
- [[Long-horizon planning]] — core algorithmic challenge.
- [[Instruction following]] ⚠️ — fundamental skill addressed by SH-VLN.
- [[Multi-task learning]] ⚠️ — related training paradigm.

---

*This page was created from source: `papers/2601.04699.pdf`.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Sequential-Horizon Vision-and-Language Navigation (SH-VLN)` --[[related_to]] ⚠️--> `Embodied AI`
