---
id: goat_bench
title: GOAT-Bench
type: concept
tags: []
confidence: 0.9
created_at: '2026-04-29T20:59:42'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
- papers/2511.10376.pdf
source_type: arxiv_paper
---

**GOAT-Bench** is a challenging benchmark for Zero-Shot Navigation and Embodied Navigation combined with Visual Question Answering ⚠️ in complex 3D environments. It provides a standardized evaluation protocol to assess navigation policies and question-answering capabilities across diverse object types, layouts, and interaction constraints, bridging the gap between simulated training and real-world deployment. The benchmark emphasizes generalizable object-aware navigation and language-guided reasoning, where an agent must locate target objects or answer spatial queries specified by natural language or category labels. Notably, GOAT‑Bench serves as a rigorous test for zero‑shot navigation scenarios, exposing failures that static benchmarks miss.

Developed as part of the research presented in the arxiv paper [2507.04047](papers/2507.04047.pdf), GOAT-Bench incorporates multi-room scenes, dynamic object placements, and realistic sensor noise. Its primary goal is to drive progress in Sim-to-Real Transfer for embodied agents by challenging methods under varied and realistic conditions.

### Key Results

- The model MTU3D achieved a **23% improvement in success rate** over the previous state-of-the-art (SOTA) on GOAT-Bench, demonstrating the benchmark’s ability to challenge and differentiate navigation and QA algorithms.
- The model MSGNav achieves **state-of-the-art performance** on GOAT‑Bench, further validating the benchmark’s utility for zero‑shot navigation tasks and reinforcing its role as a demanding evaluation platform.

### Relations

- **used_by**: MTU3D, MSGNav — Both models were evaluated on GOAT-Bench and set successive performance milestones.
- **depends_on**: Simulation Environments ⚠️, 3D Scene Datasets ⚠️ — GOAT-Bench relies on high-fidelity 3D scene assets and physics simulators.
- **part_of**: Embodied AI Benchmarking ⚠️ — GOAT-Bench contributes to the broader ecosystem of benchmarks for embodied agents.
- **implements**: Object Navigation Metrics ⚠️, Visual Question Answering Metrics ⚠️ — The benchmark defines specific metrics such as success rate, SPL (Success weighted by Path Length), object detection recall, and answer accuracy. For zero‑shot navigation, additional metrics such as generalization gap and unseen‑scene success rate are emphasized.