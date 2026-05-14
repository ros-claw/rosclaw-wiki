---
id: human_attention_in_navigation
title: Human Attention in Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:09:33'
last_reinforced: '2026-04-29T21:09:33'
supersedes: []
sources:
- papers/2205.12219.pdf
source_type: arxiv_paper
---

## Human Attention in Navigation

**Human Attention in Navigation** refers to the visual attention patterns of a human follower during wayfinding tasks. In the context of embodied AI, it is the recorded gaze or focus of a person as they navigate an environment following natural language instructions. This concept is formalized in the AVDN Dataset, where human attention is captured as part of the navigation data.

### Parameters

- **Role**: Follower’s visual attention during navigation — the observer's gaze that indicates which parts of the scene are relevant for decision-making.
- **Data Collection**: Recorded as part of the AVDN Dataset using head-mounted eye tracking. The attention map is a continuous heatmap of where the human looked over time.
- **Utilization**: Used by HAA-Transformer to predict waypoints. The model integrates attention input to infer the most probable next step in navigation.

### Capabilities

- **Enhance navigation prediction accuracy** — Human attention provides additional grounding, reducing ambiguity in instruction following.
- **Provide interpretability for model decisions** — By correlating model attention with human attention, the system becomes more transparent.

### Relationships

- **`used_in`**: HAA-Transformer
- **`depends_on`**: Human visual perception ⚠️, Attention mechanisms ⚠️

### Importance

Human attention serves as a strong supervisory signal for learning navigation policies that are both efficient and explainable. It bridges the gap between raw visual input and high-level task goals, making it a central concept in the field of Embodied AI.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Human Attention in Navigation` --related_to ⚠️ ⚠️ ⚠️--> `AVDN Dataset`
- `Human Attention in Navigation` --related_to ⚠️ ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Human Attention in Navigation` --related_to ⚠️ ⚠️ ⚠️--> `HAA-Transformer` _(wikilink)_
