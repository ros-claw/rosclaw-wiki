---
id: imagenav_image_goal_navigation
title: ImageNav (Image Goal Navigation)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:38:16'
last_reinforced: '2026-04-29T20:38:16'
supersedes: []
sources:
- papers/2509.16445.json
source_type: arxiv_paper
---

## ImageNav (Image Goal Navigation)

**ImageNav**, short for **Image Goal Navigation**, is a embodied AI task where an agent must navigate to a location that is specified by a target image. The agent receives a first-person view and a static goal image (e.g., a photo of a particular room or object), and must move through the environment until its current observation sufficiently matches the target image.

This task is distinct from point-goal or language-goal navigation because the goal is represented visually rather than geometrically or verbally. It requires the agent to perform visual matching, spatial reasoning, and long-horizon planning.

### Capabilities

- Navigate to a location specified by a single goal image, even when the starting point is far away and the environment is partially observable.

### Role in Training Mixtures

ImageNav is a key component of the [[FiLM-Nav]] training data mixture. Its inclusion helps train navigation policies that can generalize across multiple goal modalities. The visual goal signal from ImageNav complements other tasks such as [[ObjectNav]] or [[LangNav]] ⚠️ within the mixture, improving the model’s ability to handle diverse goal representations.

### Relationships

- `part_of` → [[FiLM-Nav training data mixture]] ⚠️ — ImageNav samples are mixed with other navigation tasks during policy training.
- `depends_on` → [[visual matching]] ⚠️ and [[spatial reasoning]] ⚠️ — the agent must compare its current view with the goal image and maintain a mental map of explored areas.
- `contrasts_with` → [[PointGoal Navigation]] ⚠️ and [[Language Goal Navigation]] ⚠️ — the goal is given as an image rather than coordinates or natural language.

### See Also

- [[Embodied AI navigation benchmarks]] ⚠️
- [[Goal-conditioned reinforcement learning]] ⚠️
- [[Sim-to-real transfer for visual navigation]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `ImageNav (Image Goal Navigation)` --[[related_to]] ⚠️--> `FiLM-Nav` _(wikilink)_
