---
id: hm3d
title: HM3D
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T23:58:06'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.16445.pdf
- papers/2505.23019.pdf
source_type: arxiv_paper
---

## HM3D (Habitat-Matterport 3D)

**HM3D** (Habitat-Matterport 3D) is a large-scale dataset of high‑quality, photorealistic 3D reconstructions of real indoor spaces. It provides realistic, **multi‑floor** environments for simulated navigation tasks and is widely used as a benchmark for embodied AI agents, particularly in **object‑goal navigation**.

### Description

HM3D consists of thousands of scanned interiors (apartments, offices, houses, multi‑story buildings) converted into fully traversable 3D meshes with semantic annotations. Many scenes span **multiple floors**, enabling evaluation of navigation policies in stair‑connected or split‑level layouts. The dataset is designed for **ObjectGoal Navigation** and **Open‑Vocabulary Object Navigation (OVON)**, allowing agents to navigate toward objects specified by language or image queries. Its high visual fidelity, structural diversity, and multi‑floor complexity make it a standard testbed for sim‑to‑real transfer in embodied AI.

### Benchmarks

- **HM3D ObjectNav** – Classic object‑goal navigation where the agent must locate a specific category (e.g., "chair") in an unseen scene.
- **HM3D‑OVON** – Open‑vocabulary variant where object targets are described by free‑form language (e.g., "the red mug on the kitchen counter").

Both benchmarks are used to evaluate navigation policies in the [[Habitat Simulator]]. HM3D is also employed as an **object‑goal navigation benchmark** for evaluating newer methods such as [[ASCENT]] (source: `papers/2505.23019.pdf`).

### Relationships

- Used by [[FiLM-Nav]] as the primary evaluation environment for ObjectNav and OVON tasks.
- Used by [[ASCENT]] for evaluation of multi‑floor, language‑specified navigation.
- Part of the broader [[Habitat]] ecosystem, which includes the habitat‑lab framework and habitat‑sim simulator.
- Supplements other datasets such as [[Matterport3D]] ⚠️ with higher‑resolution reconstructions and expanded room coverage.

### Key Capabilities

- Provides realistic 3D scans with continuous action spaces for policy learning.
- Supports both discrete‑step (teleport) and continuous‑movement navigation.
- Includes semantic segmentation and object‑bounding boxes for supervision.
- Offers **multi‑floor** environments with stairs and vertical connectivity, relevant for advanced navigation benchmarks.

### References

- Defined in the Habitat‑Matterport 3D Dataset paper (Ramakrishnan et al., 2021).
- Used in evaluation of [[ASCENT]] (source: `papers/2505.23019.pdf`).
- For usage in FiLM‑Nav, see [[FiLM-Nav]] and associated paper (source: `papers/2509.16445.pdf`).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Pending review:**
- `HM3D` --[[related_to]] ⚠️--> `FiLM-Nav` _(wikilink)_
- `HM3D` --[[used_in]] ⚠️--> `ASCENT` _(wikilink)_