---
id: dynamic_bounded_memory_queue
title: Dynamic Bounded Memory Queue
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:08:29'
last_reinforced: '2026-04-30T00:08:29'
supersedes: []
sources:
- papers/2511.06840.pdf
source_type: arxiv_paper
---

# Dynamic Bounded Memory Queue

The **Dynamic Bounded Memory Queue** is a memory structure that stores past navigation states to inform future actions. It functions as a bounded and dynamic memory queue within a larger decision-making framework.

## Description

The queue records exploration history, allowing the system to maintain context over time while respecting a fixed capacity (bounded). Its dynamic nature means it can adaptively manage which states are retained, prioritizing information relevant to current goals. By incorporating past states, it helps avoid local deadlocks by enabling the agent to recall and escape dead-end configurations.

## Parameters

- **Type**: Memory queue
- **Property**: Bounded and dynamic

## Capabilities

- **Incorporates exploration history** – enables the system to leverage previous navigation states for improved decision-making.
- **Avoids local deadlocks** – prevents the agent from repeatedly entering the same dead-end situations by retaining knowledge of past failures.

## Relationships

- **part_of** → [[Memory-guided Decision-Making mechanism]] ⚠️  
  The queue is a core component of a larger mechanism that uses memory to inform step-by-step decisions.
- **used_by** → [[PanoNav]]  
  The queue is employed by the PanoNav system to guide navigation tasks.

## See also

- [[Navigation]] ⚠️
- [[Exploration Strategy]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Dynamic Bounded Memory Queue` --[[related_to]] ⚠️--> `PanoNav` _(wikilink)_
