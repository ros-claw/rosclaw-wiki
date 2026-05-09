---
id: oracle_success_rate_osr
title: Oracle Success Rate (OSR)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:33:54'
last_reinforced: '2026-04-30T00:33:54'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

### Oracle Success Rate (OSR)

**Oracle Success Rate (OSR)** is a metric used in [[Vision-and-Language Navigation]] (VLN) to relax the strict success criterion of standard [[Success Rate (SR)]]. Instead of requiring the agent to stop exactly at the goal location, OSR considers an episode successful if the goal is reachable from **some point along the agent’s traversed path**. This allows for navigation errors that still place the agent within a feasible approach zone to the target.

#### Definition

> **OSR** = Percentage of episodes where the goal is reachable (i.e., lies within a predefined spatial threshold) from at least one viewpoint visited by the agent during its route.

The metric was introduced to decouple trajectory‑planning quality from exact final‑position precision, providing a more forgiving evaluation that still captures meaningful navigation competence.

#### Role in Evaluation

- **Measures** the agent’s ability to bring the goal within reach, even if it fails to stop precisely at the target.
- **Complements** [[Success Rate (SR)]] and [[Success weighted by Path Length (SPL)]] by isolating path‑planning effectiveness from localization accuracy.
- **Used as evaluation metric in** [[OpenVLN]], where it enables comparison of navigation systems that prioritize broad coverage over pinpoint localization.

#### Usage in OpenVLN

In the [[OpenVLN]] framework (source: `papers/2511.06182.pdf`), OSR serves as a key performance indicator. The paper reports that OpenVLN improves OSR by **up to 6.19%** over prior methods, indicating that its open‑vocabulary grounding allows agents to consistently traverse paths that bring the goal within reach, even when exact stopping poses are missed.

#### Related Concepts

- [[Success Rate (SR)]] – stricter metric requiring the agent to stop at the goal.
- [[Success weighted by Path Length (SPL)]] – penalizes inefficient paths even if successful.
- [[Goal Reachability]] ⚠️ – general notion underlying OSR.
- [[Navigation Error Metrics]] ⚠️ – broader category of evaluation measures.

> **Relationship annotations**  
> - `OSR` → `used_as_evaluation_metric_in` → [[OpenVLN]]  
> - `OpenVLN` → `implements` → OSR (as one of its evaluation criteria)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Oracle Success Rate (OSR)` --[[related_to]] ⚠️ ⚠️--> `Vision-and-Language Navigation`
**Pending review:**
- `Oracle Success Rate (OSR)` --[[related_to]] ⚠️ ⚠️--> `OpenVLN` _(wikilink)_
