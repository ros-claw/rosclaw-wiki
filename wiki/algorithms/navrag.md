---
id: navrag
title: NavRAG
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:57:30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2502.11142.pdf
source_type: arxiv_paper
---

---

# NavRAG

**NavRAG** is a retrieval-augmented generation framework for embodied navigation instruction generation. It addresses limitations of previous step-by-step instruction generation by leveraging a [[Large Language Model (LLM)]] ⚠️ ⚠️ ⚠️ to produce diverse navigation instructions that match user communication styles. At its core, the framework builds a **hierarchical scene description tree** from 3D scenes and uses a [[Retrieval-Augmented Generation (RAG)]] mechanism to tailor instructions to different user roles and requests.

## Method

NavRAG operates in two stages. First, a [[Large Language Model (LLM)]] ⚠️ ⚠️ ⚠️ constructs a hierarchical scene description tree that captures the 3D scene from its global layout down to local details. Second, the system simulates various user roles with specific navigation demands and retrieves relevant branches from this scene tree to generate instructions that reflect those users' communication styles and informational needs.

## Data Generation

The framework has been used to annotate **over 2 million navigation instructions** across **861 scenes**. This large-scale dataset supports training and evaluation in [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ tasks.

## Capabilities

- Generates user-demand instructions for Vision-and-Language Navigation
- Simulates various user roles with specific demands
- Builds a hierarchical scene description tree for 3D scene understanding
- Retrieves from hierarchical scene description tree to generate context-aware instructions
- Annotates over 2 million navigation instructions across 861 scenes

## Dependencies & Relationships

- **Uses:** [[Large Language Model (LLM)]] ⚠️ ⚠️ ⚠️, [[Retrieval-Augmented Generation (RAG)]]
- **Depends on:** [[3D scene understanding]] ⚠️, hierarchical scene description tree, [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️

## References

- ArXiv paper 2502.11142 — *NavRAG: Retrieval-Augmented Generation for Embodied Navigation Instruction Generation*