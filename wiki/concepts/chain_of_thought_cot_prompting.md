---
id: chain_of_thought_cot_prompting
title: Chain-of-Thought (CoT) Prompting
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:40:56'
last_reinforced: '2026-04-29T20:40:56'
supersedes: []
sources:
- papers/2504.09000.json
source_type: arxiv_paper
---

## Chain-of-Thought (CoT) Prompting

**Chain-of-Thought (CoT) Prompting** is a reasoning technique for large language models that decomposes complex tasks into a sequence of intermediate reasoning steps. In the context of embodied intelligence, CoT elicits structured, step-by-step reasoning that improves both perception and decision-making in robotic systems. The hierarchical variant, **Hierarchical Chain-of-Thought (H-CoT)**, further organizes reasoning into multiple levels of abstraction, enabling the extraction of compositional knowledge through iterative reasoning.

### Mechanism

CoT operates in a multi-turn QA style where each step builds on the previous reasoning, allowing the model to structure its internal computation by decomposing a high-level goal (e.g., "locate a target object") into subgoals (e.g., "first find the room → then check the table → identify the object"). This mirrors the human cognitive process of locating a target object, where attention is directed hierarchically: from region to furniture to item.

### Capabilities

- **Improved perception**: By reasoning stepwise, the model can incrementally integrate sensor data and semantic cues, reducing ambiguity in object detection and scene understanding.
- **Enhanced decision-making**: Compositional reasoning chains allow the agent to evaluate multiple possible actions (e.g., "walk forward → stop → look left") before committing to a plan, leading to more robust navigation and manipulation.

### Relationships

- **Used by**: CL-CoTNav – implements H-CoT to perform continual learning of navigation policies, extracting compositional knowledge from success/failure traces.
- **Inspired by**: Human cognitive search strategies – especially the process of narrowing down a target's location via spatial and categorical hierarchies.
- **Relates to**: Embodied AI for task planning, Hierarchical RL ⚠️ for options decomposition, and Visual Language Models ⚠️ for grounding language instructions in visual observations.

### Source

This page derives from the paper *"CL-CoTNav: Continual Learning for Chain-of-Thought Navigation"* (arXiv:2504.09000), which introduces H-CoT as a core mechanism for compositional reasoning in embodied agents.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Chain-of-Thought (CoT) Prompting` --related_to ⚠️--> `CL-CoTNav` _(wikilink)_
