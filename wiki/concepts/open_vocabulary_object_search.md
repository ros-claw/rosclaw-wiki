---
id: open_vocabulary_object_search
title: Open-Vocabulary Object Search
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:34:49'
last_reinforced: '2026-04-29T20:34:49'
supersedes: []
sources:
- papers/2602.19308.json
source_type: arxiv_paper
---

## Open-Vocabulary Object Search

**Open-Vocabulary Object Search** is the ability for a robot to search for and navigate to any object described by natural language, without prior training on specific object classes. It combines semantic understanding with geometric navigation to enable robots to find arbitrary objects in unstructured outdoor environments, operating without prior maps or pre-enumerated object categories.

### Capabilities

- Enables robots to find arbitrary objects in unstructured outdoor environments.
- Combines semantic understanding with geometric navigation.
- Operates without prior maps or pre-enumerated object categories.

### Dependencies

This concept **depends_on**:

- [[Foundation models]] – for zero-shot language understanding and visual grounding.
- [[Semantic reasoning]] – to interpret natural language queries and relate them to sensory data.
- [[Geometric exploration]] ⚠️ – to plan and execute efficient search trajectories in unknown spaces.

### Implementations

The primary known implementation is **[[WildOS]]**, which **implements** Open-Vocabulary Object Search in the context of long-range autonomous navigation.

### Importance

Open-vocabulary object search is crucial for long-range autonomous tasks such as search-and-rescue, environmental monitoring, and logistics in unknown terrains. By removing the need for pre-trained object catalogs, it greatly expands the adaptability of robotic systems to real-world, open-ended scenarios.

---

*Source: arxiv paper `papers/2602.19308.json`*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Open-Vocabulary Object Search` --[[related_to]] ⚠️--> `WildOS` _(wikilink)_
