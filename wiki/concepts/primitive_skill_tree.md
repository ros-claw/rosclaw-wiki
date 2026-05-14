---
id: primitive_skill_tree
title: Primitive Skill Tree
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:51:18'
last_reinforced: '2026-04-30T03:51:18'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

# Primitive Skill Tree

A **Primitive Skill Tree** is a structured representation of discrete, atomic actions or skills that an embodied agent can perform. It organizes these skills in a tree hierarchy, enabling a reasoning system — typically powered by a large language model (LLM) — to determine the optimal sequence and target objects for task execution.

## Description

The Primitive Skill Tree framework encodes low-level robot capabilities (e.g., pick, place, push, grasp) into nodes of a tree. Each node may contain attributes such as preconditions, effects, and associated object affordances. By traversing this tree, an LLM-based planner can decompose high-level instructions into ordered sequences of primitive skills, reasoning about which objects to interact with and in what order. This structure bridges the gap between abstract language input and concrete robot actions.

## Capabilities

- **Task planning with large language models** – The tree serves as a structured action space that constrains LLM reasoning to feasible, primitive-level steps.
- **Facilitates effective reasoning to determine interaction objects and sequences** – The hierarchical organization allows the planner to recursively decompose tasks and select appropriate objects at each stage.

## Relationships

- `used_by` → AINav – The AINav system employs the Primitive Skill Tree to plan navigation and manipulation tasks.
- `implements` → Task Planning with LLMs ⚠️ ⚠️ – This method realizes the broader concept of Task Planning with LLMs ⚠️ ⚠️ by providing a concrete skill representation for LLM-based decomposition.

## Notes

The tree is typically designed offline based on robot capabilities and environment constraints, then reused across multiple tasks. It is a key component in systems that combine language understanding with embodied execution.