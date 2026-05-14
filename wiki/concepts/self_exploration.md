---
id: self_exploration
title: Self-exploration
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:06:54'
last_reinforced: '2026-04-30T02:06:54'
supersedes: []
sources:
- papers/2203.04006.pdf
source_type: arxiv_paper
---

## Self-exploration

**Self-exploration** is the ability of an embodied agent to autonomously sample trajectories within its environment, generating training data without any form of human supervision or labeling. It is a core enabler for algorithms that must learn from scratch in the deployment domain, eliminating the need for pre-collected or human-demonstrated datasets.

### Capabilities

*   Enables autonomous trajectory sampling – the agent decides which states and actions to visit based on its own current policies or curiosity drives.
*   Generates training data without human supervision – removes the bottleneck of manual data collection and annotation.

### Relationships

*   **Implemented by** → ProbES (Probabilistic Exploration with Self-supervision), which uses self-exploration to build in-domain datasets for downstream policy learning.

### See also

*   Exploration vs Exploitation ⚠️
*   Sim-to-Real Transfer
*   Reinforcement Learning

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Self-exploration` --related_to ⚠️--> `ProbES` _(wikilink)_
