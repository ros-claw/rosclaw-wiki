---
id: object_level_sub_goals
title: Object-Level Sub-Goals
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:41:41'
last_reinforced: '2026-04-29T21:41:41'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

# Object-Level Sub-Goals

## Definition

**Object-Level Sub-Goals** are semantically meaningful navigation targets defined at the object level — e.g., "go to the chair" — rather than coordinate-based or geometric waypoints. They enable an agent to decompose complex navigation tasks into interpretable, reusable steps that generalize across environments.

This concept is central to [[Embodied AI]] systems that require zero-shot transfer between different spaces. By abstracting goals to object classes or instances, the agent can plan and execute without retraining on each new layout.

## Capabilities

- **Semantically meaningful navigation goals**: The agent can interpret natural-language-like commands (e.g., “move to the table”) and ground them to perceptual objects.
- **Zero-shot generalization to novel environments**: Because the goal is defined relative to object categories (not absolute coordinates), the same sub-goal works in any scene containing that object, enabling immediate deployment without fine-tuning.

## Usage

Object-Level Sub-Goals are used by the [[TANGO]] system, which leverages them as intermediate steps in long-horizon tasks. TANGO dynamically generates such sub-goals from a high-level instruction, then executes each with a low-level policy.

## Related Concepts

- [[Goal-Conditioned Reinforcement Learning]] ⚠️ — often uses state-based or position-based goals; object-level sub-goals provide a complementary semantic abstraction.
- [[Semantic Mapping]] ⚠️ — required to locate objects in the environment and feed them into the sub-goal planner.
- [[Hierarchical Task Decomposition]] ⚠️ — object-level sub-goals naturally fit into a layered architecture where high-level reasoning selects object targets and low-level control reaches them.

## Notes

The concept is drawn from the paper [2509.08699](data/raw/papers/2509.08699.pdf), which demonstrates that object-level sub-goals improve interpretability and sample efficiency in vision-language navigation tasks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Object-Level Sub-Goals` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Object-Level Sub-Goals` --[[related_to]] ⚠️ ⚠️--> `TANGO` _(wikilink)_
