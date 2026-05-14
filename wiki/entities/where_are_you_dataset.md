---
id: where_are_you_dataset
title: Where Are You? Dataset
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:55:20'
last_reinforced: '2026-04-30T02:55:20'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

## Where Are You? Dataset

The **Where Are You? (WAY) dataset** is a collection of approximately 6,000 human–human dialogs designed to study cooperative localization in 3D environments. It involves two agents—an **Observer** and a **Locator**—who collaborate to locate the Observer’s position on a top-down map.

---

### Overview

The WAY dataset provides a testbed for embodied communication and spatial reasoning. The Observer is spawned at a random location in a 3D environment and can navigate using first-person views while answering the Locator’s questions. The Locator must localize the Observer on a detailed **top-down map** by asking questions and giving instructions. This creates a natural dialog setting that requires reference resolution, perspective-taking, and grounding in both visual and map-based representations.

---

### Dataset Details

- **Size:** ~6,000 dialogs  
- **Task:** Cooperative localization  
- **Agents:** Observer (answers questions, navigates in 3D), Locator (asks questions, interprets map)  
- **Environment:** 3D scene with a corresponding top-down map  
- **Input modalities:** First-person RGB views (Observer), map (Locator), dialog history  

The Observer and Locator roles are clearly separated, forcing the agents to disambiguate spatial language and build joint understanding of the environment.

---

### Tasks Supported

The dataset defines three distinct tasks, each highlighted in the original paper:

1. **Localization from Embodied Dialog (LED)** — The Locator must locate the Observer based solely on dialog history and map information.
2. **Embodied Visual Dialog** — The Observer must answer visual questions about its surroundings while the Locator uses those answers to infer location.
3. **Cooperative Localization** — Both agents actively communicate and act to determine the Observer’s position.

These tasks benchmark different aspects of spatial awareness, dialog grounding, and cooperative reasoning.

---

### Relationships

- **Used by:** Localization from Embodied Dialog (LED), Embodied Visual Dialog, Cooperative Localization
- **Depends on:** 3D environment ⚠️, top-down map ⚠️

---

### See Also

- Human-Robot Dialog Datasets ⚠️  
- Spatial Language Grounding ⚠️  
- Sim-to-Real Transfer for Localization ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Where Are You? Dataset` --related_to ⚠️--> `Localization from Embodied Dialog (LED)`
