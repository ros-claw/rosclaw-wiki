---
id: embodiedbench
title: EmbodiedBench
type: entity
tags: []
confidence: 0.9
created_at: '2026-04-29T21:20:54'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2502.09560.pdf
- articles/article.md
source_type: arxiv_paper
---

# EmbodiedBench

**EmbodiedBench** is a comprehensive benchmark designed to evaluate vision-driven embodied agents, with a special focus on Multi-modal Large Language Models (MLLMs). It comprises **1,128 testing tasks** distributed across **4 distinct environments** and **6 meticulously curated subsets**, providing a multifaceted standardized evaluation platform for embodied intelligence. The benchmark was published as an **ICML 2025 Oral** paper (arXiv: [2502.09560](https://arxiv.org/abs/2502.09560)).

## Overview

EmbodiedBench is a comprehensive benchmark for evaluating MLLMs as embodied agents across high-level and low-level tasks with fine-grained capability evaluation. It provides a multifaceted, standardized evaluation platform. The environments are organized into two tiers:

- **High-level tasks** (EB-ALFRED, EB-Habitat): require complex instruction understanding and long-horizon planning.
- **Low-level tasks** (EB-Navigation, EB-Manipulation): test spatial awareness, visual perception, and fine-grained motor control.

The six curated subsets systematically assess essential agent capabilities: commonsense reasoning, complex instruction understanding, spatial awareness, visual perception, long-term planning, and basic task solving.

## Key Facts

| Property      | Value                                                                 |
|---------------|-----------------------------------------------------------------------|
| Total tasks   | 1,128                                                                 |
| Environments  | 4 — EB-ALFRED, EB-Habitat, EB-Navigation, EB-Manipulation |
| Subsets       | 6 — commonsense reasoning, complex instruction understanding, spatial awareness, visual perception, long-term planning, basic task solving |
| Published at  | ICML 2025 Oral                                                        |
| arXiv ID      | [2502.09560](https://arxiv.org/abs/2502.09560)                        |

## Subsets

The six curated subsets ensure broad coverage of agent capabilities:

- **Commonsense reasoning** – evaluate everyday physical and social knowledge.
- **Complex instruction understanding** – test parsing of multi‑step, ambiguous commands.
- **Spatial awareness** – assess understanding of object locations and spatial relations.
- **Visual perception** – evaluate object recognition, attribute detection, and scene understanding.
- **Long-term planning** – measure ability to generate and execute extended action sequences.
- **Basic task solving** – benchmark fundamental success on simple goal‑oriented tasks.

## Capabilities

EmbodiedBench is designed to evaluate agents across a broad spectrum of skills:

- Basic task solving
- Commonsense reasoning
- Complex instruction understanding
- Spatial awareness
- Visual perception
- Long-horizon planning

The benchmark enables systematic comparison of agent capabilities across different environmental conditions and difficulty levels. It specifically targets two categories of performance:

- **High-level semantic tasks** – e.g., household activities requiring language grounding and planning.
- **Low-level atomic tasks** – e.g., navigation and manipulation requiring precise motor control.

## Key Findings

Evaluation of 24 leading MLLMs (including GPT-4o ⚠️ ⚠️ and 23 others) reveals a significant performance gap:

- MLLMs **excel at high-level tasks** such as EB-ALFRED and EB-Habitat, demonstrating strong language understanding and planning.
- They **struggle substantially with low-level manipulation** tasks, where the best model (GPT-4o) achieved only **28.9% average success rate** across all tasks.
- This disparity highlights the need for improved perceptual‑motor grounding in vision‑language systems.

## Leaderboard

The benchmark evaluates leading MLLMs, including GPT-4o ⚠️ ⚠️, Claude-3.5-Sonnet ⚠️, Gemini-1.5-pro ⚠️, InternVL2.5-78B ⚠️, and **23 other models**. Performance is reported separately for high-level tasks (EB-ALFRED, EB-Habitat) and low-level tasks (EB-Navigation, EB-Manipulation), enabling fine-grained comparison of reasoning versus perceptual-motor capabilities. GPT-4o leads overall but remains far from human-level performance on low-level control.

## Usage

Researchers use EmbodiedBench to:

- Quantify the generalization and robustness of embodied agents.
- Benchmark new vision‑language action (VLA) models.
- Identify failure modes in perception, planning, and control pipelines.
- Compare high-level reasoning performance against low-level execution fidelity.

The benchmark is publicly available and includes code for task execution, data collection, and automated scoring.

## Relationships

- **evaluates** → MLLMs (Multi‑Modal Large Language Models) and other vision‑language models.
- **uses** → Multi-modal Large Language Models (MLLMs) ⚠️ as the primary agent architecture under test.
- **depends_on** → the four core environments (EB-ALFRED, EB-Habitat, EB-Navigation, EB-Manipulation), each of which may build upon standard simulators like Habitat, ManipStation ⚠️, or iGibson ⚠️.
- **part_of** → the broader ecosystem of embodied AI benchmarks, alongside ALFRED ⚠️, EQA ⚠️, and BEHAVIOR ⚠️.
- **implements** → a systematic task taxonomy and evaluation protocol that supports reproducibility and cross‑model comparison.

---

*See also: VLA Models ⚠️, Sim-to-Real Transfer, Embodied AI Evaluation ⚠️.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EmbodiedBench` --depends_on ⚠️ ⚠️ ⚠️ ⚠️--> `EB-ALFRED`
- `EmbodiedBench` --depends_on ⚠️ ⚠️ ⚠️ ⚠️--> `EB-Habitat`
- `EmbodiedBench` --depends_on ⚠️ ⚠️ ⚠️ ⚠️--> `EB-Navigation`
- `EmbodiedBench` --depends_on ⚠️ ⚠️ ⚠️ ⚠️--> `EB-Manipulation`