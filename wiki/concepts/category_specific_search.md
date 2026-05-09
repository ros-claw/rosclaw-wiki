---
id: category_specific_search
title: Category-Specific Search
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:58:54'
last_reinforced: '2026-04-29T20:58:54'
supersedes: []
sources:
- papers/2412.05552.pdf
source_type: arxiv_paper
---

## Category-Specific Search

**Category-Specific Search** is a high-level navigation task type within [[Instruction-Guided Visual Navigation]] in which an embodied agent must locate an object or place matching a given category description (e.g., "find a sofa") by actively exploring an unknown environment. It contrasts with [[Low-Level Language-Guided Navigation]] ⚠️ ⚠️ by focusing on scene-level reasoning and object recognition rather than step-by-step movement commands.

### Description

Category-Specific Search requires the agent to interpret a category-level instruction, plan an exploration strategy, and identify candidate regions or objects that satisfy the query. The task emphasizes:
- **Exploration process** – the agent cannot rely on a known map; it must decide where to move and how to search efficiently.
- **Object recognition** – once an area is reached, the agent uses visual perception to classify objects and determine if they match the target category.
- **High-level semantics** – the instruction refers to a category rather than a specific instance, requiring generalization (e.g., recognizing any chair, not a particular one).

This paradigm is central to applications like domestic service robots, autonomous search-and-rescue, and warehouse retrieval where the target is described by type rather than exact location.

### Capabilities

- Emphasizes exploration process to locate objects or places matching a category description.
- High-level navigation task type — the agent determines the search strategy and low-level actions autonomously.

### Relationships

| Type | Page | Description |
|------|------|-------------|
| **part_of** | [[Instruction-Guided Visual Navigation]] | Category-Specific Search is a specific task variant within the broader family of navigation guided by natural language instructions. |
| **contrasts_with** | [[Low-Level Language-Guided Navigation]] ⚠️ ⚠️ | Whereas low-level navigation gives step‑by‑step instructions ("turn left", "go forward 5 meters"), category‑specific search provides a goal category and leaves exploration to the agent. |

### See Also

- [[Object Goal Navigation]] (a closely related task where the goal is a specific object class)
- [[Exploration Strategy]] ⚠️
- [[Visual Place Recognition]] ⚠️
- [[Semantic SLAM]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Category-Specific Search` --[[related_to]] ⚠️--> `Instruction-Guided Visual Navigation`
