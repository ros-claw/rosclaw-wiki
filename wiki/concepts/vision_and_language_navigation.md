---
id: vision_and_language_navigation
title: vision_and_language_navigation
type: concept
tags: []
confidence: 0.95
created_at: '2026-04-29T21:06:00'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2403.07376.pdf
- papers/2304.04907.pdf
- papers/1806.02724.pdf
source_type: arxiv_paper
---

# Vision-and-Language Navigation

Vision-and-Language Navigation (VLN) is a task where an agent navigates through a physical or simulated environment by following natural language instructions. As a crucial research problem of **[[embodied_ai]]**, VLN requires an embodied agent to perceive its surroundings via visual input, comprehend language commands, and select from a set of navigable locations at each step to reach a target destination—all without explicit maps or predefined routes. The agent must ground language in visual observations and make decisions at a high level, inferring missing low-level motor commands from context, such as how to turn, move forward, or stop.

## Task Formulation

VLN is an **embodied AI task** (type: `navigation with natural language instructions`). At each time step, the agent receives a natural language instruction and an egocentric visual observation; it must select the next action from an **action space** defined as the set of navigable locations available at that step. The agent must integrate multimodal understanding and spatial reasoning in real-time, inheriting the core challenges of Embodied AI: grounding language, memory, planning, and adaptation to dynamic environments.

## Capabilities

- Requires an embodied agent to navigate through 3D environments following natural language instructions.
- Requires understanding of both vision and language, bridging perception and instruction.
- The agent selects its next action from a set of navigable locations at each step.
- The agent must infer low-level motor commands (e.g., turning angles, step distances) from the high‑level navigable location choices.

## Environments

VLN agents are evaluated in **complex 3D** environments, typically photorealistic indoor scenes or simulated realistic worlds. A common platform is **Matterport3D**, which provides large-scale, photorealistic indoor environments for training and evaluation.

## Benchmarks

Standard benchmarks include:

- **Room-to-Room (R2R)** — the foundational VLN dataset built on Matterport3D.
- **Room-across-Room (RxR)** — extends R2R with longer, multilingual instructions.
- **Room-for-Room (R4R) ⚠️** — a variant focusing on diversity in path instructions.
- **CVDN (Cooperative Vision-and-Dialog Navigation)** — a dataset that combines dialogue and navigation, evaluating an agent's ability to follow instructions in a collaborative setting.

These benchmarks test instruction-following and spatial reasoning across varying environmental complexity and instruction length.

## Dependencies and Usage

- **Direct inputs**: The agent receives and uses Natural Language Instructions ⚠️ and Visual Perception ⚠️ as its primary inputs.
- **Depends on**: Natural Language Processing ⚠️ for instruction comprehension, Computer Vision ⚠️ for visual perception.
- **Uses**: LLM ⚠️, [[large_language_model]] — modern VLN systems often leverage large language models for instruction comprehension, reasoning, and action planning. Additionally, advanced VLN methods exploit **future-view semantics** to anticipate upcoming visual observations and improve navigation decisions.

## Relationships

- **Part of**: [[embodied_ai]]
- **Used by**: VLN-SIG — a special interest group that coordinates research and benchmarks in this area.
- **Evaluated on**: Room-to-Room (R2R) dataset, CVDN dataset.

## Related Pages

- Embodied AI — parent concept
- Large Language Model — supporting technology
- Visual Navigation — closely related task without explicit language grounding
- Instruction Following ⚠️ — broader paradigm
- Matterport3D ⚠️ — common simulation environment for VLN

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `vision_and_language_navigation` --related_to ⚠️ ⚠️ ⚠️--> `embodied_ai`
- `vision_and_language_navigation` --related_to ⚠️ ⚠️ ⚠️--> `Embodied AI`
- `vision_and_language_navigation` --related_to ⚠️ ⚠️ ⚠️--> `Room-across-Room (RxR)`