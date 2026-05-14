---
id: kv_cache_reuse
title: KV Cache Reuse
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:55:43'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.05240.pdf
source_type: arxiv_paper
---

# KV Cache Reuse

## Description

KV Cache Reuse is a memory optimization technique employed in StreamVLN to enable coherent multi-turn dialogue while maintaining a **bounded context size** and controlled inference cost. It leverages reused key-value (KV) caches from previous turns, avoiding full recomputation of long sequences and thereby enabling fast, scalable dialogue streaming. This mechanism is a core component of both the fast-streaming dialogue context ⚠️ ⚠️ architecture and StreamVLN's slow-fast design ⚠️ ⚠️.

## Parameters

| Parameter | Value |
|-----------|-------|
| context_size | bounded |

## Capabilities

- Enables efficient multi-turn dialogue by reusing cached key-value pairs, retaining relevant history without unbounded input length.
- Limits context size and inference cost in long video streams by avoiding redundant attention computations.
- Reduces inference cost for long sequences by avoiding redundant attention computations.

## Relationships

- **used_by**: StreamVLN — StreamVLN depends on KV Cache Reuse to maintain long-context coherence in real-time navigation dialogues.
- **part_of**: fast-streaming dialogue context ⚠️ ⚠️ — KV Cache Reuse is a building block of the larger fast-streaming dialogue system.
- **part_of**: StreamVLN's slow-fast design ⚠️ ⚠️ — KV Cache Reuse is a key enabler of the slow (high-frequency) streaming path in StreamVLN's hybrid architecture.

## Source

This page is derived from the research described in arxiv paper **2507.05240**.

<!-- Cross-reference: see also KV Cache ⚠️, Inference Optimization ⚠️, Multi-turn Dialogue ⚠️ -->

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `KV Cache Reuse` --extends ⚠️--> `StreamVLN`