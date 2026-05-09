---
id: template_based_instruction_generator
title: Template-based instruction generator
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:29:07'
last_reinforced: '2026-04-30T02:29:07'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

## Template-based Instruction Generator

A **Template-based instruction generator** is an [[Algorithm]] ⚠️ that produces navigational instructions for robots or agents by filling predefined sentence templates with spatial and object information. It represents a rule-based approach to natural language generation for human-robot interaction, serving as a baseline for more sophisticated methods.

### Overview

Template-based generators operate by defining a set of syntactic frames (e.g., "Turn left at the [landmark]") and populating them with extracted entities from the environment (e.g., "couch", "door", "table"). This approach ensures grammatical correctness and explicit control over output structure, at the cost of limited variability and naturalness.

### Capabilities

- Generates [[Navigation Instructions]] ⚠️ using fixed templates.
- Guarantees instruction comprehensibility by constraining output to known grammar patterns.
- Suitable for controlled, low-resource environments where training data for neural methods is scarce.

### Comparison

The template-based instruction generator has been **compared_with** the following approaches:

- **[[Automatic Instruction Generators]] ⚠️** – These include neural sequence-to-sequence models (e.g., LSTM-based or Transformer-based generators) that learn to produce instructions from demonstration or vision. Template-based generators are simpler, more interpretable, and require no training, but yield less diverse and less context-aware output.
- **[[Human Instructors]] ⚠️** – Human-written instructions are natural, context-rich, and adaptive. The template method falls short in flexibility and expressiveness but can be preferred for consistency and repeatability in benchmarking.

| Aspect | Template-based | Automatic (neural) | Human |
|--------|----------------|--------------------|-------|
| **Training required** | None | Large dataset | N/A |
| **Variability** | Low | High | Very high |
| **Interpretability** | High | Low | High |
| **Robustness** | High (rule-governed) | Medium | Medium |

### Limitations

- Cannot handle novel object references or syntactic variations outside the template set.
- Often produces repetitive or unnatural phrasing.
- Requires manual engineering of templates and extraction of relevant entities.

### Sources

- Primary: [[arXiv:2101.10504]] ⚠️ *"Comparing Template-based and Automatic Instruction Generators for Robot Navigation"* (2021).

### See Also

- [[Automatic Instruction Generation]] ⚠️
- [[Human Instruction Following]] ⚠️
- [[Embodied Question Answering]] ⚠️
- [[Sim-to-Real Transfer]] (for instruction generation evaluation)