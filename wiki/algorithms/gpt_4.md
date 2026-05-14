---
id: gpt_4
title: GPT-4
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-30T01:21:05'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2401.07314.pdf
- papers/2502.09560.pdf
source_type: arxiv_paper
---

# GPT-4o

GPT-4o is a proprietary multimodal large language model (MLLM) developed by OpenAI ⚠️, serving as the cognitive core for embodied agents. It builds upon the capabilities of GPT-4 and GPT-4V ⚠️, adding native multimodality across text, vision, and audio. In robotics and embodied AI, GPT-4o functions as a high-level planner and reasoning engine, enabling agents to interpret natural language instructions, process visual inputs, and generate complex action sequences.

## GPT-4V (Vision Variant)

GPT-4V extends GPT-4 with multimodal (vision-and-language) understanding. It can process visual inputs such as camera images, maps, or environmental layouts alongside textual commands, making it especially suitable for embodied navigation tasks. In architectures like MapGPT, GPT-4V is prompted with a map representation of the environment to generate zero-shot navigation plans—without any finetuning on the target environment.

## GPT-4o (Omni)

GPT-4o is the latest iteration from OpenAI, integrating vision, language, and audio understanding into a single model. It is part of the broader family of Multi-modal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️. Compared to GPT-4V, GPT-4o offers improved efficiency and native support for multiple modalities without separate processing pipelines.

### Performance on EmbodiedBench

In the comprehensive EmbodiedBench evaluation (covering high-level planning, low-level manipulation, and navigation tasks across 24 MLLMs), GPT-4o achieved the **highest average score of 28.9%**. It excelled at high-level tasks such as task decomposition and abstract reasoning, but **struggled with low-level manipulation tasks** that require fine-grained motor control or precise spatial awareness. This performance gap highlights a common limitation of current MLLMs in grounding high-level reasoning to precise physical actions.

## Role in Embodied AI

GPT-4 and its variants function as the central decision-making component in high-level planning pipelines. While the base model handles language-only reasoning, GPT-4V and GPT-4o bring visual grounding and multimodal understanding to the same role, allowing agents to interpret visual context (e.g., obstacles, landmarks) and produce executable action sequences. They replace or augment traditional planning modules with broad world knowledge and reasoning abilities, achieving extraordinary flexibility in novel scenarios.

## Capabilities

- **Extraordinary decision-making**: GPT-4o can evaluate multiple action options and select optimal strategies based on prior knowledge and current context.
- **Multimodal understanding**: GPT-4o processes text, images, and audio, enabling reasoning about spatial relationships, environmental layouts, and spoken commands.
- **Zero-shot navigation planning when prompted with a map**: GPT-4V and GPT-4o can generate step-by-step navigation instructions from natural language goals when presented with a map of the environment—even for unseen environments.
- **Generalization across tasks**: Without fine-tuning, GPT-4o applies learned patterns from its training data to new manipulation, navigation, and interaction tasks.
- **Top performance among MLLMs on EmbodiedBench**: GPT-4o achieved 28.9% average, best among 24 evaluated models, but exhibits limited ability in low-level manipulation.
- **Zero-shot reasoning for navigation planning**: Both GPT-4 and GPT-4o can generate step-by-step navigation instructions from natural language goals in the text domain; vision variants extend this to visually grounded contexts.

## Relationships

- **Depends on**: Large Language Models (as foundational technology), Transformer Architecture ⚠️, Multi-modal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️.
- **Part of**: Multi-modal Large Language Models (MLLMs) ⚠️ ⚠️ ⚠️.
- **Used by**: MapGPT — MapGPT depends on GPT-4, GPT-4V, and GPT-4o for decision-making and planning. The vision variants are particularly leveraged when map images are provided as input.
- **Evaluated in**: EmbodiedBench — GPT-4o achieved the highest average score (28.9%) among 24 MLLMs.
- **Related to**: Embodied AI, Zero-shot Learning, Foundation Models for Robotics ⚠️, Multimodal Learning ⚠️

## Sources

- arxiv paper `2401.07314` — "MapGPT: Map-Guided Prompting for Embodied Agent Planning" (GPT-4V employed as the brain of the embodied agent, using map images for zero-shot navigation).
- arxiv paper `2502.09560` — "EmbodiedBench: Comprehensive Evaluation of Multi-modal Large Language Models for Embodied Agents" (GPT-4o evaluated, achieving 28.9% average, best among 24 MLLMs).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GPT-4o` --extends ⚠️--> `GPT-4`
- `GPT-4o` --part_of ⚠️--> `Multi-modal Large Language Models (MLLMs)`
- `GPT-4o` --evaluated_in ⚠️--> `EmbodiedBench`
- `EmbodiedBench` --benchmark_for ⚠️--> `GPT-4o`