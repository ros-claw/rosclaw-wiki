---
id: navgpt
title: NavGPT
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:22:36'
last_reinforced: '2026-04-30T01:22:36'
supersedes: []
sources:
- papers/2305.16986.pdf
source_type: arxiv_paper
---

## NavGPT

**NavGPT** is a purely LLM-based instruction-following navigation agent designed for **zero-shot sequential action prediction** in Vision-and-Language Navigation (VLN). By leveraging the reasoning abilities of large language models like ChatGPT ⚠️ ⚠️ ⚠️ and GPT-4, NavGPT demonstrates explicit reasoning in complex embodied scenes without requiring fine-tuning or task-specific training.

### Overview

NavGPT treats VLN as a language reasoning problem. It takes **textual descriptions of visual observations**, the agent’s **navigation history**, and a set of **future explorable directions** as input, and outputs high-level navigation actions. The model decomposes natural language instructions into sub‑goals, incorporates commonsense knowledge, identifies landmarks, tracks progress, and adapts to unexpected situations by adjusting plans. Additionally, NavGPT can generate high-quality navigational instructions and draw accurate top‑down metric trajectories of completed paths.

### Parameters

| Parameter | Value |
|-----------|-------|
| Base models | ChatGPT ⚠️ ⚠️ ⚠️, GPT-4 |
| Input modalities | Textual descriptions of visual observations, navigation history, future explorable directions |
| Task | Zero‑shot sequential action prediction for Vision-and-Language Navigation |

### Capabilities

- High-level planning for navigation  
- Decompose instructions into manageable sub‑goals  
- Integrate commonsense knowledge into decision making  
- Identify landmarks from observed scenes  
- Track navigation progress and remaining steps  
- Adapt to exceptions with plan adjustments (e.g., obstacle avoidance)  
- Generate high-quality navigational instructions from trajectories  
- Draw accurate top‑down metric trajectories of completed paths  

### Relationships

- **uses** → LLMs ⚠️ ⚠️, ChatGPT ⚠️ ⚠️ ⚠️, GPT-4  
- **applied_to** → Vision-and-Language Navigation  
- **depends_on** → LLM reasoning capabilities ⚠️  

### How It Works (Conceptual)

1. **Perception → Text**: Visual observations from the agent’s camera are converted into textual scene descriptions (e.g., object names, spatial relationships).  
2. **Instruction Parsing**: The natural language instruction (e.g., "Walk past the sofa, turn right at the table, and stop in front of the window") is broken into sub‑goals.  
3. **Action Selection**: NavGPT selects the next action (e.g., move forward, turn, stop) from a set of candidates, guided by the sub‑goal and current scene.  
4. **Progress Tracking**: The agent’s history is fed back to maintain context and detect goal completion.  
5. **Exception Handling**: If the perceived scene contradicts expectations (e.g., a blocked path), NavGPT revises its plan.

### Significance

NavGPT illustrates that general‑purpose language models, without any specialized training, can serve as embodied navigation agents. Its success highlights the potential of LLMs ⚠️ ⚠️ for grounding language in real‑world environments and opens the door to using commonsense reasoning for robot navigation tasks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `NavGPT` --based_on ⚠️--> `Vision-and-Language Navigation`
