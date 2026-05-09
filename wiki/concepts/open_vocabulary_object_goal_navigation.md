---
id: open_vocabulary_object_goal_navigation
title: Open-vocabulary object-goal navigation
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T00:03:14'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02400.pdf
- papers/2507.06747.pdf
source_type: arxiv_paper
---

## Open-Vocabulary Object-Goal Navigation

### Definition

Open-vocabulary object-goal navigation refers to the ability of a robotic system to locate and navigate to objects described in open-set natural language (e.g., “find a red cup”) without relying on a fixed set of object categories. Agents must generalize to novel objects unseen during training in unseen environments, operating without prior knowledge of object categories.

### Capabilities

- **Navigate toward objects specified by arbitrary natural language descriptions** – The agent handles queries that refer to objects not seen during training.
- **Locate novel objects in unseen environments** – Generalization beyond trained classes and layouts.
- **Operate without prior knowledge of object categories** – No closed set of object labels is assumed; agents use natural language or visual descriptions to identify targets.

### Related Concepts

- [[Object-Goal Navigation]] – The base task, extended here to open-vocabulary settings.
- [[Embodied AI]] – The broader field of intelligence situated in physical agents.
- [[Vision-Language Models]] ⚠️ ⚠️ – Used to align visual observations with textual or conceptual queries.
- [[Zero-shot Learning]] – Agents transfer knowledge to unseen object categories.
- [[Sim-to-Real]] ⚠️ – Training in simulation with domain randomization to enable real-world open-vocabulary performance.

### Approaches

Open-vocabulary navigation typically combines:
1. **Visual grounding** – e.g., [[CLIP]]-based detectors that match image regions to arbitrary text queries.
2. **Semantic mapping** – Building spatial memory with object-centric representations.
3. **Exploration policies** – Learned or heuristic strategies to cover the environment efficiently.
4. **Language-conditioned planning** – Using natural language instructions or goal descriptions to guide the agent.

A recent example is [[LOVON]], a method that implements open-vocabulary navigation through learned open-vocabulary object pointers and a hierarchical exploration policy.

### Challenges

- **Open-world generalization** – Agents must handle object appearances, viewpoints, and backgrounds unseen in training.
- **Data sparsity** – Hard to collect enough examples of all possible objects.
- **Real-time inference** – Vision-language models can be computationally expensive on robot hardware.
- **Ambiguity** – Natural language queries may be vague (e.g., “find something to drink” vs. “find a red cup”).

### Standard Benchmarks

Common evaluation suites include [[HM3D ObjectNav]] ⚠️, [[Gibson ObjectNav]] ⚠️, and [[Habitat Open Vocabulary ObjectNav]] ⚠️, where agents are tested on novel object categories held out from training.

### Relationship Annotations

- *uses* → [[Vision-Language Models]] ⚠️ ⚠️
- *depends_on* → [[Object-Goal Navigation]]
- *implements* → [[Zero-shot Learning]] in embodied contexts
- *part_of* → [[Embodied AI]]
- *implemented_by* → [[LOVON]]

*For further details, see the sources: arXix 2512.02400 and arXix 2507.06747.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Open-vocabulary object-goal navigation` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Open-vocabulary object-goal navigation` --[[related_to]] ⚠️ ⚠️--> `CLIP` _(wikilink)_