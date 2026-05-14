---
id: spice
title: SPICE
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T01:17:34'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.08467.pdf
- papers/2101.10504.pdf
source_type: arxiv_paper
---

## SPICE

**SPICE** (Semantic Propositional Image Caption Evaluation) is a metric originally designed for evaluating image captioning quality by comparing semantic propositions. In the context of embodied instruction generation, SPICE has been adapted to measure the **semantic similarity** between a generated instruction and a reference instruction. It quantifies how well the generated instruction captures the core meaning, objects, relationships, and actions required for a task. SPICE relies on **reference instructions** as the ground‑truth against which generated instructions are evaluated.

### Parameters

| Parameter | Value |
|-----------|-------|
| **Metric for** | Instruction Generation ⚠️ ⚠️ quality |
| **Value improvement** | 23.5 → 26.2 (using SRDF ⚠️ ⚠️ ⚠️) |

The improvement from a baseline SPICE score of 23.5 to 26.2 was achieved through the application of **SRDF ⚠️ ⚠️ ⚠️** (Structure‑aware Reward Diffusion Framework), which refines the generation policy to better align with semantic correctness.

### Capabilities

- Evaluates **semantic similarity** of generated instructions against ground‑truth references.
- Captures propositional content (objects, attributes, relations) beyond simple n‑gram overlap.
- Provides a fine‑grained score that correlates with human judgment of instruction quality.
- Recommended for ranking instruction generation systems when reference instructions are available.

### Related Concepts

- Metric ⚠️ – higher‑level category for evaluation measures.
- SRDF ⚠️ ⚠️ ⚠️ – implements reward shaping that directly improves SPICE scores during training.
- Instruction Generation ⚠️ ⚠️ – the task for which SPICE serves as an evaluation metric.
- Semantic Similarity ⚠️ – the core property assessed by SPICE.
- Reference Instructions ⚠️ – the ground‑truth input required by SPICE (implied usage).

### References

- *Paper: arxiv 2412.08467* – introduces the use of SPICE within SRDF to enhance instruction generation for embodied agents.