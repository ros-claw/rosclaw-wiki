---
id: spl
title: SPL
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:40'
last_reinforced: '2026-04-29T23:58:40'
supersedes: []
sources:
- papers/2509.16445.pdf
source_type: arxiv_paper
---

## SPL (Success weighted by Path Length)

SPL is a standard metric used in **navigation evaluation** that jointly measures the **success rate** and **path length efficiency** of a robot's navigation. It is widely adopted in embodied AI benchmarks (e.g., Habitat, Matterport3D) to penalize overly long but successful paths.

### Definition

SPL combines success rate with path length efficiency. For a set of navigation episodes, it is defined as:

\[
\text{SPL} = \frac{1}{N} \sum_{i=1}^N S_i \cdot \frac{L_i^*}{\max(L_i, L_i^*)}
\]

where:
- \( S_i \) = 1 if episode \( i \) succeeded, 0 otherwise
- \( L_i^* \) = optimal (shortest) path length to goal
- \( L_i \) = actual path length taken by the agent

A higher SPL (range 0–1) indicates that the agent not only succeeds frequently but also finds **efficient, near‑optimal paths**.

### Relationship to Other Metrics

- **success rate ⚠️** (SR) – SPL incorporates SR as a binary factor, but penalizes long paths even when successful. Agents with high SR but overly long trajectories will have lower SPL.
- **Normalized Dynamic Time Warping (NDTW)** – Another navigation metric that measures path similarity beyond discrete success, though SPL remains the most common single‑number metric in sim‑to‑real navigation.

### Usage

SPL is used as the primary evaluation metric in many embodied navigation systems, including **FiLM‑Nav ⚠️**, where it measures the efficiency of the visual‑language navigation pipeline. It is also a key metric in benchmarks like **Habitat** and **PointGoal Navigation ⚠️**.

---

*See also: evaluation metrics in embodied AI ⚠️, sim‑to‑real transfer ⚠️*