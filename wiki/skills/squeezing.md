---
id: squeezing
title: Squeezing
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T00:20:12'
last_reinforced: '2026-04-30T00:20:12'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

### Squeezing

**Squeezing** is a navigational skill that enables an agent to traverse narrow spaces that are only marginally wider than its own dimensions. It involves precise motion planning and control to avoid collisions while passing through constricted passages.

#### Capabilities

- **Navigational ability to squeeze through narrow spaces** — The agent can evaluate gaps, orient itself, and execute a safe, collision-free trajectory through confined openings. This skill is essential for exploring cluttered environments or accessing areas blocked by obstacles.

#### Learning Source

Squeezing is **learned_from** an Reinforcement Learning Expert ⚠️ specifically trained in a squeezing-dense environment. The expert demonstrates optimal behavior for tight passages, which is then distilled into the agent's policy.

#### Role in MM-Nav

Squeezing is a core component of the **MM-Nav** (Multi-Modal Navigation) system. It is **part_of** the suite of capabilities that allow MM-Nav to handle diverse terrain and obstacle configurations. Without squeezing, the navigator would be unable to exploit short routes through narrow corridors or between closely spaced objects.

#### Related Skills

- Local Obstacle Avoidance ⚠️ — complements squeezing by providing reactive collision avoidance.
- Path Planning in Constrained Spaces ⚠️ — higher-level planning that invokes squeezing when needed.

---

*Source: papers/2510.03142.pdf*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Squeezing` --uses ⚠️--> `MM-Nav`
