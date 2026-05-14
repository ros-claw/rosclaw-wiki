---
id: hm3d_ovon
title: HM3D-OVON
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:21'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

## HM3D-OVON

**HM3D-OVON** (Habitat-Matterport 3D Open-Vocabulary Object Navigation) is a benchmark dataset and evaluation framework for embodied navigation tasks that require agents to locate arbitrary objects specified by natural language in photorealistic 3D environments. It extends the Habitat-Matterport 3D ⚠️ ⚠️ (HM3D) dataset with open-vocabulary object navigation goals, enabling rigorous evaluation of vision-language navigation models. Additionally, HM3D-OVON supports embodied question-answering evaluations, broadening its scope beyond pure object navigation.

### Overview

The benchmark is designed to assess an agent’s ability to navigate towards objects described in natural language (e.g., "find a red mug") without being restricted to a fixed set of object classes. It builds upon the HM3D dataset of high-resolution 3D scans of real indoor spaces, adding semantic annotations and goal definitions that are diverse and compositional. HM3D-OVON provides a standardized evaluation protocol including success rate, coverage, and efficiency metrics. Its design also accommodates question-answering tasks, where agents must answer queries about their environment after navigation, making it a versatile tool for Embodied AI research.

### Key Facts

- **Type:** Benchmark for Open-Vocabulary Object Navigation ⚠️ ⚠️ and embodied question-answering
- **Domain:** Embodied navigation (photorealistic 3D environments)
- **Related system:** MTU3D – a model that achieved a **14% improvement in success rate** over the state-of-the-art on the HM3D-OVON benchmark.
- **Source:** Paper 2507.04047 (*likely title: "MTU3D: Multimodal Transformer for Open-Vocabulary Navigation"*)
- **Core dependencies:** Embodied AI, Habitat Simulator, Large Language Models (for language grounding)

### Relationship Annotations

| Relationship | Target Entity | Description |
|--------------|---------------|-------------|
| `is_a` | Embodied Navigation Benchmark ⚠️ | HM3D-OVON is a specific instance of a navigation benchmark. |
| `extends` | Habitat-Matterport 3D ⚠️ ⚠️ | Adds open-vocabulary object goal annotations to HM3D scenes. |
| `used_by` | MTU3D | Used as the primary evaluation benchmark for the MTU3D model. |
| `implements` | Open-Vocabulary Object Navigation ⚠️ ⚠️ | Provides the evaluation infrastructure for this task. |
| `depends_on` | Habitat Simulator | Relies on the Habitat simulator for rendering and physics. |

### Usage

HM3D-OVON is typically used to:

- Evaluate open-vocabulary navigation policies in realistic indoor environments.
- Assess embodied question-answering models that integrate navigation and language understanding.
- Compare vision-language navigation models (e.g., MTU3D, VLN-BERT, CLIP-based policies).
- Benchmark advancements in language grounding, scene understanding, and goal-directed exploration.

### Related Concepts

- Close-Set Object Navigation ⚠️
- Vision-and-Language Navigation (VLN)
- Zero-Shot Navigation
- Sim-to-Real Transfer in Embodied AI ⚠️
- Embodied Question Answering ⚠️

### References

- Paper: *"MTU3D: Multimodal Transformer for Open-Vocabulary Object Navigation"* (arXiv:2507.04047)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HM3D-OVON` --related_to ⚠️ ⚠️ ⚠️--> `Embodied AI`
- `HM3D-OVON` --related_to ⚠️ ⚠️ ⚠️--> `Vision-and-Language Navigation`
**Pending review:**
- `HM3D-OVON` --related_to ⚠️ ⚠️ ⚠️--> `CLIP` _(wikilink)_