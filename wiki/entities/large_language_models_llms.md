---
id: large_language_models_llms
title: Large Language Models (LLMs)
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-29T20:50:36'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.13729.pdf
- papers/2506.01551.pdf
- papers/2502.11142.pdf
- papers/2312.02010.pdf
source_type: arxiv_paper
---

**Large Language Models (LLMs)** are a class of deep learning models trained on vast text corpora (e.g., general text from the internet), capable of understanding, generating, and reasoning with natural language. In the context of embodied intelligence and robotics, LLMs serve as a central reasoning engine for tasks such as planning, communication, adaptive strategy generation, navigational decision support, and **retrieval-augmented instruction generation**. Their remarkable semantic understanding and generation abilities across various fields make them a promising foundation for embodied navigation.

#### Role in Multi-Robot & Navigation Systems

In systems like **[[SayCoNav]]**, **[[EvolveNav]]**, and **[[NaviLLM]]**, the LLM functions as a decision-making hub that:

- Generates collaboration strategies automatically, adapting to dynamic environments and mission objectives.
- Produces step-by-step plans for each robot, converting high-level goals into actionable sequences.
- Processes shared information (e.g., sensor data, status reports) to continuously refine and update plans.
- Supports **navigational decision making**, especially in vision-language navigation (VLN) tasks, where the LLM reasons over visual and linguistic inputs to guide robot movement.

LLMs also serve as the base model for **[[NaviLLM]]**, where their broad language comprehension is directly adapted for embodied navigation tasks, bridging general language understanding with spatial reasoning.

#### Role in Retrieval-Augmented Navigation (NavRAG)

In the **[[NavRAG]]** framework, the LLM takes on two specialized roles:

- **Building a scene description tree** — Given a 3D environment, the LLM constructs a hierarchical representation of the scene, capturing spatial layout and object relationships.
- **Generating diverse natural-language instructions** — Using the scene tree and retrieved contextual information, the LLM produces user-directed navigation instructions that are both **grounded in the 3D layout** and **adaptable to varying user demands**.

This retrieval-augmented generation (RAG) approach combines the LLM’s broad language capabilities with external knowledge to produce more accurate and context‑aware instructions.

#### Capabilities

The LLM contributes the following core capabilities to robotic systems:

- **Reasoning ability** — performs logical deduction and multi-step planning.
- **Language understanding and generation** — interprets human instructions and produces coherent messages; demonstrates remarkable semantic understanding and generation across various fields.
- **Navigational decision support** — helps resolve ambiguity in route selection and goal interpretation.
- **Automatically generate collaboration strategies** — no pre-programmed rules required; strategy emerges from reasoning over the current state.
- **Generate step-by-step plans for each robot** — decomposes complex missions into per-agent execution steps.
- **Process shared information to update plans** — interprets incoming data from teammates and revises plans in real time.
- **Understands 3D scene layouts** — capable of parsing spatial geometry and semantic content to build hierarchical scene descriptions.
- **Generates diverse natural language instructions** — produces varied instruction sets that suit different user needs and environmental contexts.
- **Supports retrieval-augmented generation (RAG)** — integrates external knowledge bases to ground outputs in real‑world data, improving accuracy and reducing hallucination.

#### Characteristics & Domain Adaptation

- **Training corpus**: general text, which provides broad world knowledge but introduces a **domain gap** when applied to specific tasks such as VLN. The model must be fine-tuned or prompted to bridge the gap between generic language understanding and task-specific spatial reasoning.
- **Open source**: Many LLMs used in robotics research are open‑source, allowing customization and deployment on local hardware. This is a key enabler for systems like EvolveNav and NaviLLM.
- **RAG compatibility**: LLMs can be paired with retrieval modules to dynamically inject task‑specific or environment‑specific knowledge, a technique central to NavRAG.
- **Base model potential**: LLMs provide a strong base for domain‑specific models like **_NaviLLM_**, which adapts general language capabilities to embodied navigation through additional training or architectural modifications.

#### Relationships

- **Used by**: [[SayCoNav]], [[EvolveNav]], [[NavRAG]], [[NaviLLM]] — core reasoning engine for navigation, collaboration, and instruction generation.
- **Improves**: [[Vision-Language Navigation (VLN)]] — LLMs enhance spatial reasoning and instruction following.
- **Depends on**: [[Natural Language Processing]] ⚠️, [[Deep Learning]] ⚠️ — for language understanding and generation.
- **Implements**: [[Collaboration Strategy]] ⚠️ generation — provides a flexible, learned approach to multi-robot coordination.

> **Note on automatic linkers**: A heuristic entity linker previously reported `Large Language Models (LLMs) --[[uses]] ⚠️--> SayCoNav`, but the correct relationship (as documented above) is the reverse: LLMs are *used by* SayCoNav. Users should verify automatically generated links.

#### Future Considerations

As LLMs grow more capable, their integration into real-time robotics will require careful management of latency, prompt engineering, and safety constraints. The ability to handle ambiguous instructions and novel scenarios makes them a promising but evolving component of embodied AI. The domain gap between general pre‑training and robotic tasks remains an active area of research, with techniques such as fine-tuning, in-context learning, hybrid architectures, and retrieval-augmented generation (RAG) being explored. RAG in particular offers a path to grounding LLM outputs in external, verifiable data — a crucial step for safety‑critical navigation tasks.

#### Summary

LLMs provide a promising foundation for embodied navigation due to their general language comprehension and generation abilities. Their semantic understanding across fields, combined with techniques like RAG and domain‑specific adaptation (e.g., in [[NaviLLM]]), makes them a versatile and powerful component in modern robotics systems.