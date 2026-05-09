---
id: large_vision_language_models_lvlm
title: Large Vision-Language Models (LVLM)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T00:38:23'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.17221.pdf
- papers/2402.15852.pdf
source_type: arxiv_paper
---

---

# Large Vision-Language Models (LVLM)

**Large Vision-Language Models (LVLMs)** are multimodal AI systems that integrate visual perception with natural language understanding, enabling them to process images and text jointly at scale. These models typically combine a vision encoder (e.g., CLIP, ViT) with a large language model (LLM) backbone, allowing for tasks such as visual question answering, image captioning, and reasoning over visual scenes.

In the context of embodied AI, LVLMs serve as high-level reasoning engines that translate visual observations into goal-directed actions. They are especially valuable for [[Embodied Navigation]] where the model must interpret complex environments and execute step-by-step instructions. A key advantage of these models is that they can achieve state‑of‑the‑art navigation performance **without requiring explicit maps or depth estimation**, relying instead on learned visual‑language correspondences.

## Video-based Variant

A natural extension of static image VLMs is the **video‑based** variant, which processes streams of consecutive frames rather than single snapshots. This temporal awareness allows the model to reason about motion, short‑term dynamics, and visual continuity — capabilities essential for real‑time navigation. In the [[NaVid]] framework, a video‑based VLM processes the agent’s live video stream to produce navigation decisions, effectively replacing traditional mapping and depth pipelines with a unified, map‑free reasoning system.

## Capabilities

- **Drive embodied navigation**: LVLMs can directly inform navigation policies by grounding natural language instructions in visual input, enabling agents to follow commands in unfamiliar environments.
- **Enhance task-specific reasoning through data-efficient, reward-driven post-training**: By fine-tuning with reinforcement learning from human or simulated rewards, LVLMs improve their performance on downstream tasks without requiring massive task-specific datasets.
- **Map‑free and depth‑free navigation**: Video‑based VLMs, as used in [[NaVid]], achieve competitive navigation results without any explicit map representation or depth sensor, simplifying the perception pipeline and generalizing to novel environments.
- **Process video streams for decision‑making**: The model ingests a continuous video feed, allowing it to detect obstacles, recognize changes in the scene, and adjust its path without frame‑by‑frame state estimation.

## Relationships

- **Used by**: [[VLN-R1]] — a framework that leverages LVLMs for vision-and-language navigation tasks, applying reward-driven post-training to boost navigation reasoning. `depends_on`
- **Base technology for**: [[NaVid]] — a navigation agent that uses a video‑based VLM as its core perception engine, achieving state‑of‑the‑art results without map or depth inputs. `base_technology_for`

## Key Papers

- The foundational capabilities described here are drawn from the paper *"VLN-R1: Reward-Driven Post-Training for Vision-and-Language Navigation"* (arXiv:2506.17221), which demonstrates how LVLMs can be effectively adapted to embodied navigation through data-efficient reinforcement learning.
- The video‑based variant and its map‑free performance are detailed in the paper *"NaVid: Video‑based VLM drives map‑free navigation"* (arXiv:2402.15852), which shows that a single video‑vision‑language model can replace the traditional mapping and planning stack in indoor navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Large Vision-Language Models (LVLM)` --[[related_to]] ⚠️--> `VLN-R1` _(wikilink)_
- `Large Vision-Language Models (LVLM)` --[[base_technology_for]] ⚠️--> `NaVid` _(wikilink)_