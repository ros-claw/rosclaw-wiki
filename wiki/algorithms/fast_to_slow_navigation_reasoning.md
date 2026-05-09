---
id: fast_to_slow_navigation_reasoning
title: Fast-to-Slow Navigation Reasoning
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:52:30'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.13733.pdf
source_type: arxiv_paper
---

## Fast-to-Slow Navigation Reasoning

**Fast-to-Slow Navigation Reasoning** (FSR) is a navigation reasoning strategy within the [[FSR-VLN]] architecture that combines efficient candidate screening with language-driven refinement for visual-language navigation (VLN). It addresses the computational bottleneck of real-time goal selection by performing a rapid initial match over candidate spaces (rooms, views, objects) and then applying a [[VLM]] ⚠️ ⚠️-driven analysis to select the most appropriate final goal.

### Mechanism

FSR first performs **fast matching** to efficiently select candidate rooms, views, and objects, then applies **VLM-driven refinement** for final goal selection. Slow reasoning is activated only when fast intuition fails — this conditional mechanism ensures that the system only invokes computationally expensive language grounding when lightweight heuristics cannot produce a confident decision. The two-stage design balances speed and semantic reasoning: the fast matching stage reduces the search space to a manageable set, while the VLM stage leverages rich language grounding to decide among the remaining candidates or to resolve ambiguous cases.

### Capabilities

- **Fast matching for candidate selection** — efficiently narrows down candidate rooms, views, and objects using lightweight similarity or nearest-neighbor techniques.
- **VLM-driven refinement for final goal selection** — uses a visual language model to evaluate the shortlisted candidates and select the most contextually appropriate goal based on natural language instructions and visual observations.
- **Activates slow reasoning only when fast intuition fails** — preserves computational efficiency by deferring to the VLM only when the fast matching stage yields low confidence or ambiguous results.

### Relationships

- **part_of** → [[FSR-VLN]]
- **uses** → [[VLM]] ⚠️ ⚠️ (Visual Language Model)

### References

- Source: arxiv paper `papers/2509.13733.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Fast-to-Slow Navigation Reasoning` --[[extends]] ⚠️--> `FSR-VLN`