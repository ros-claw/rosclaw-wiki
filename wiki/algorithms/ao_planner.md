---
id: ao_planner
title: AO-Planner
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:58:59'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

---

## AO-Planner

**AO-Planner** is an affordances-oriented planning algorithm for continuous vision-and-language navigation (VLN) that integrates multiple foundation models to achieve zero-shot navigation in unseen environments. The system combines visual affordances prompting with a dedicated path agent to bridge high-level decision-making and low-level motion control.

### Overview

AO-Planner integrates various foundation models to achieve affordances-oriented low-level motion planning and high-level decision-making, both in a zero-shot setting. It achieves state-of-the-art zero-shot performance on the [[R2R-CE]] and [[RxR-CE]] benchmarks, with an 8.8% improvement on **SPL** (Success weighted by Path Length) on R2R-CE. The system uses a modular architecture that separates semantic reasoning from motion execution, enabling robust navigation without task-specific training.

### Capabilities

- **Zero-shot continuous VLN** – performs navigation tasks without any fine-tuning on the target dataset.
- **Affordances-oriented low-level motion planning and high-level decision-making** – interprets scene affordances to guide both action selection and trajectory generation.
- **Waypoint prediction** – generates sub-goals or waypoints from high-level language instructions using affordance-aware prompting.
- **Data annotation via pseudo-labels** – can produce pseudo-labeled training data to improve downstream models or alternative pipelines.
- **8.8% improvement on SPL on R2R-CE** – establishes a new state of the art for zero-shot methods on this benchmark.
- **State-of-the-art zero-shot performance on R2R-CE and RxR-CE** – outperforms prior zero-shot baselines across all standard VLN metrics on both datasets.

### Architecture

AO-Planner uses two core components:

- **Visual Affordances Prompting** – a module that takes visual input (RGB images, depth, camera intrinsics) and generates affordance-aware prompts for the LLM.
- **PathAgent** – a low-level motion planner that executes paths inferred from the affordance prompts in continuous space.

The system relies on a stack of foundation models:

- [[SAM]] ⚠️ ⚠️ – segmenting objects and regions of interest from visual input.
- [[LLM]] ⚠️ ⚠️ – reasoning about navigation goals and generating natural language plans.
- Depth information and camera intrinsic parameters – used to project 2D affordances into 3D space for motion planning.

### Dependencies

| Dependency | Type |
|------------|------|
| Visual Affordances Prompting | uses |
| PathAgent | uses |
| [[SAM]] ⚠️ ⚠️ | uses |
| [[LLM]] ⚠️ ⚠️ | uses |
| depth information | uses, depends_on |
| camera intrinsic parameters | uses, depends_on |

### Performance

On the [[R2R-CE]] dataset, AO-Planner achieves:

- **SPL**: +8.8% over previous zero-shot state-of-the-art
- **Success Rate**: competitive with fully-supervised methods despite being **zero-shot**

On the [[RxR-CE]] dataset, AO-Planner also holds state-of-the-art zero-shot results, demonstrating strong cross-dataset generalization without any fine-tuning.

The model does not require any parameter updates or dataset-specific tuning, making it directly applicable to new environments.

### Related Work

- [[VLN-BERT]] – prior work using BERT for vision-language navigation
- [[CLIP]] – used in some zero-shot navigation pipelines
- [[Continuous VLN]] ⚠️ – the problem setting AO-Planner addresses

### References

- *AO-Planner: Affordances-Oriented Planning for Zero-Shot Continuous Vision-Language Navigation* (arXiv:2407.05890)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `AO-Planner` --[[implements]] ⚠️ ⚠️--> `R2R-CE`
- `AO-Planner` --[[implements]] ⚠️ ⚠️--> `RxR-CE`