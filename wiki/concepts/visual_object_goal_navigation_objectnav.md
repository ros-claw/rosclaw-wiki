---
id: visual_object_goal_navigation_objectnav
title: Visual Object Goal Navigation (ObjectNav)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:40:19'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2504.09000.pdf
- papers/2504.09000.json
source_type: arxiv_paper
---

## Visual Object Goal Navigation (ObjectNav)

**Visual Object Goal Navigation** (often abbreviated as *ObjectNav*) is a fundamental task in Embodied AI where an agent must locate a specified target object in an unseen environment using only egocentric visual observations. ObjectNav requires a robot to find a specific object in a novel environment without prior maps or training, relying solely on onboard perception. The primary challenge is generalization to unseen scenes and novel objects that were not encountered during training.

### Parameters
- **Task**: locate a target object in an unseen environment using egocentric observations.
- **Challenge**: generalization to unseen scenes and novel objects.

### Capabilities
- Navigation to target object — the agent must explore, recognize objects, and navigate efficiently to reach the specified goal.

ObjectNav serves as a benchmark for evaluating an agent's ability to explore, recognize objects, and navigate efficiently. It is used by CL-CoTNav as a downstream task to test the effectiveness of chain-of-thought reasoning and continual learning for navigation.

### Relationships
- **Part of**: Embodied AI — ObjectNav is a canonical task within the embodied AI community, alongside tasks like point navigation and rearrangement.
- **Implemented by**: CL-CoTNav — the CL-CoTNav system uses ObjectNav as the scenario to evaluate its continual learning and chain-of-thought navigation capabilities.
- **Used by**: CL-CoTNav — (synonymous with implemented by; retained for clarity).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Visual Object Goal Navigation (ObjectNav)` --related_to ⚠️--> `CL-CoTNav` _(wikilink)_