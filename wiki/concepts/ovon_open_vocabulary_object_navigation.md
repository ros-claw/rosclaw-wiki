---
id: ovon_open_vocabulary_object_navigation
title: OVON (Open-Vocabulary Object Navigation)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:38:08'
last_reinforced: '2026-04-29T20:38:08'
supersedes: []
sources:
- papers/2509.16445.json
source_type: arxiv_paper
---

**OVON (Open-Vocabulary Object Navigation)** is a navigation task definition where an agent must locate and move to objects whose category names are provided at test time but were **not seen during training**. This tests the agent’s ability to generalize from language descriptions to physically locating novel object instances in unseen environments.

OVON is a core component of the FiLM-Nav training data mixture, providing diverse open‑vocabulary examples that force the agent to rely on visual‑language grounding rather than memorized object positions. Its inclusion makes the training distribution more robust for zero‑shot object search.

**Key capabilities:**
- Navigate to object categories never encountered during training (zero‑shot object navigation).
- Leverage language embeddings (e.g., from CLIP) to bridge the gap between novel textual descriptions and visual features.
- Operate without prior knowledge of the environment layout or object locations.

**Relationships:**
- `part_of` FiLM-Nav training data mixture.
- `depends_on` Visual‑Language Models ⚠️ for open‑vocabulary grounding.
- `implements` Open‑Vocabulary Object Navigation ⚠️ task.
- `related_to` Sim‑to‑Real ⚠️ generalization strategies.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `OVON (Open-Vocabulary Object Navigation)` --related_to ⚠️--> `FiLM-Nav` _(wikilink)_
