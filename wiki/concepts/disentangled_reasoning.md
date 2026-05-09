---
id: disentangled_reasoning
title: disentangled_reasoning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:09:14'
last_reinforced: '2026-04-29T21:09:14'
supersedes: []
sources:
- papers/2403.07376.pdf
source_type: arxiv_paper
---

# Disentangled Reasoning

**Disentangled reasoning** is a [[chain-of-thought reasoning]] paradigm for embodied navigation that decomposes the decision process into separate, interpretable stages instead of a single direct mapping from perception to action. By separating imagination, observation selection, and action determination, it improves both the transparency and the robustness of robotic movement decisions.

## Definition

Disentangled reasoning refers to breaking down the navigational decision process into separate, interpretable stages—imagination, alignment, action—rather than a single direct prediction. This structured approach allows the agent to reason about where it wants to go, what it currently sees, and how to bridge the gap, making failures easier to diagnose and correct.

## Parameters

- **Type**: [[chain-of-thought reasoning]]
- **Steps**:
  1. **Imagination** – Generate a prospective goal representation or mental image of the desired location.
  2. **Observation selection** – Align the imagined goal with current sensory input (e.g., vision, depth) to identify relevant features.
  3. **Action determination** – Compute the concrete motor commands or navigation policy to move toward the goal.

## Capabilities

- Improves action decision by separating reasoning into distinct, interpretable steps.
- Enables clearer debugging and error analysis: each step can be inspected independently.
- Facilitates transfer learning, as the sub-modules (imagination, observation selection) can be reused across tasks.

## Relationships

- **Implemented by**: [[NavCoT]] – uses disentangled reasoning as its core inference pipeline.
- **Contrasts with**: [[Direct Action Prediction]] – which collapses perception and action into a single black-box model, trading interpretability for simplicity.
- **Depends on**: [[Visual Language Models]] ⚠️ (for imagination and observation alignment), [[Embodied Navigation]] task definition.

## See Also

- [[chain-of-thought reasoning]]
- [[Imagination in Robotics]] ⚠️
- [[Interpretable Navigation]] ⚠️
- [[Sim-to-Real for VLA Models]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `disentangled_reasoning` --[[related_to]] ⚠️ ⚠️ ⚠️--> `chain-of-thought reasoning`
**Pending review:**
- `disentangled_reasoning` --[[related_to]] ⚠️ ⚠️ ⚠️--> `NavCoT` _(wikilink)_
- `disentangled_reasoning` --[[related_to]] ⚠️ ⚠️ ⚠️--> `Direct Action Prediction` _(wikilink)_
