---
id: last_mile_problem_zero_shot_navigation
title: Last Mile Problem (Zero-Shot Navigation)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:47:40'
last_reinforced: '2026-04-30T03:47:40'
supersedes: []
sources:
- papers/2511.10376.pdf
source_type: arxiv_paper
---

### Last Mile Problem (Zero-Shot Navigation)

**Also known as:** Last-Mile Navigation, Final Viewpoint Determination  

**Type:** [[concept]] ⚠️  
**Related domain:** Embodied AI, Zero-Shot Navigation, Visual Navigation  

---

#### Description

The **last mile problem** in zero-shot navigation refers to the challenge of determining the **feasible target location** with a **suitable final viewpoint** when an embodied agent approaches the goal region. Unlike classic visual navigation where a precise target pose is given, zero-shot settings demand that the agent itself infer *where* to stop and *how* to orient itself to successfully complete the task — often under partial observability and without task-specific training.

This problem is particularly acute in open-vocabulary or language-guided navigation, where the goal is described semantically (e.g., "the red chair near the window") rather than as exact coordinates. The agent must resolve ambiguity about which instance satisfies the goal and what vantage point yields a successful final observation.

---

#### Identified In

- MSGNav (Multi-Scale Geometric Navigation) ⚠️ ⚠️ — the MSGNav paper ⚠️ explicitly identifies and resolves the last mile problem with its **Visibility-based Viewpoint Decision module**.

---

#### Key Challenges

- Ambiguity in semantically specified goals
- Need for geometric reasoning about occlusion and line-of-sight
- Trade-off between stopping too early (incomplete task) and overshooting (invalid termination)
- Lack of explicit training signal for "good final viewpoints" in zero-shot paradigms

---

#### Related Concepts

- Zero-Shot Navigation — the broader problem setting in which the last mile problem arises.
- Visibility-based Viewpoint Decision — a module that explicitly resolves the last mile by scoring candidate poses based on visibility and semantic alignment.
- Goal Conditioned Reinforcement Learning ⚠️ — often used to train navigation policies, but zero-shot variants must handle last-mile reasoning without task-specific reward shaping.
- Sim-to-Real Transfer — last mile failure modes often emerge when sim-trained policies lack real-world occlusion reasoning.

---

#### Relationships

- MSGNav (Multi-Scale Geometric Navigation) ⚠️ ⚠️ `implements` a solution to this problem via its Visibility-based Viewpoint Decision module.
- This problem `depends_on` Partial Observability ⚠️ and Semantic Goal Specification ⚠️.
- Solving this problem `enables` Deployable Zero-Shot Navigation ⚠️ in cluttered environments.

---

#### References

1. MSGNav paper (arXiv 2511.10376) — Section on Visibility-based Viewpoint Decision.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Last Mile Problem (Zero-Shot Navigation)` --related_to ⚠️--> `Embodied AI`
