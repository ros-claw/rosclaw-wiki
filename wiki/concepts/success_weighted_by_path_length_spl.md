---
id: success_weighted_by_path_length_spl
title: Success weighted by Path Length (SPL)
type: concept
tags: []
confidence: 0.95
created_at: '2026-04-30T00:34:53'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.06182.pdf
- papers/2412.08467.pdf
- papers/1909.02244.pdf
- papers/2312.03275.pdf
source_type: arxiv_paper
---

---

## Success weighted by Path Length (SPL)

**Success weighted by Path Length (SPL)** is a widely used evaluation metric for navigation agent performance ⚠️ in embodied navigation tasks. It measures not only whether an agent reaches the target goal, but also penalizes inefficient (overly long) paths. Formally, SPL is defined as:

\[
\text{SPL} = \frac{1}{N} \sum_{i=1}^N S_i \cdot \frac{l_i}{\max(l_i, p_i)}
\]

Where:
- \( S_i \) is a binary indicator of success (1 if agent reaches the target, 0 otherwise),
- \( l_i \) is the length of the shortest path (ground‑truth oracle path) from start to goal,
- \( p_i \) is the actual path length taken by the agent.

Equivalently, for a single trial: SPL = success × (shortest_path_length / max(shortest_path_length, actual_path_length)). If the agent does not reach the goal, SPL = 0. This formulation balances success rate and path efficiency, rewarding agents that reach the goal via routes close to the optimal.

SPL ranges from 0 to 1. An agent that reaches the goal via the shortest path achieves SPL = 1; a successful but inefficient agent receives an intermediate score; failures score 0.

---

### Usage in Evaluations

SPL is the primary evaluation metric in the OpenVLN benchmark (an open‑source visual navigation framework). Recent improvements in OpenVLN have boosted SPL by up to **4.07%** relative to prior baselines, demonstrating more efficient path planning alongside higher success rates.

SPL is also the standard metric in the Room-to-Room (R2R) benchmark, a task where an agent must follow natural language instructions to navigate through real environments. The metric is used in conjunction with Success Rate ⚠️ ⚠️ and Path Length ⚠️ ⚠️ to fully characterize agent performance. Because SPL jointly captures success and efficiency, it is preferred over simple success percentage in many embodied AI tasks, including PointGoal Navigation ⚠️ and ObjectGoal Navigation ⚠️. It is also a core component of Navigator evaluation ⚠️ ⚠️ frameworks.

Additionally, SPL is employed in the evaluation of the **VLFM** (Vision-Language Frontier Maps) framework, where it serves as a key metric for assessing navigation efficiency and success in goal‑directed tasks. This reinforces SPL’s role as a standard in modern embodied AI systems.

Separately, using the **SRDF** (Success Rate Discount Factor) method, SPL has been reported to improve from **70% to 78%** on challenging navigation tasks, representing a substantial gain in both success and efficiency. This improvement underscores SPL’s sensitivity to algorithmic refinements that jointly optimize path length and goal-reaching.

---

### Related Concepts

- Navigation Metrics ⚠️ — broader discussion of evaluation methods in embodied AI.
- Path Length ⚠️ ⚠️ — the raw distance traveled; a component of SPL.
- Success Rate ⚠️ ⚠️ — the binary success component used in SPL.
- Embodied AI — the field that standardizes metrics like SPL.
- Navigator evaluation ⚠️ ⚠️ — evaluation pipelines that rely on SPL as a primary metric.
- Room-to-Room (R2R) benchmark — a visual‑language navigation benchmark where SPL is the standard metric.
- VLFM — a vision‑language frontier mapping framework that uses SPL for evaluation.

*Sources: arxiv:2511.06182 (OpenVLN), arxiv:2412.08467 (SRDF improvements), and VLFM evaluation (from arxiv paper 2312.03275)*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Success weighted by Path Length (SPL)` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Success weighted by Path Length (SPL)` --related_to ⚠️ ⚠️--> `OpenVLN` _(wikilink)_
- `Success weighted by Path Length (SPL)` --used_by ⚠️--> `Navigator evaluation` _(wikilink)_