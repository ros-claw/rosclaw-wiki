---
id: object_detection
title: Object Detection
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:25:29'
last_reinforced: '2026-04-30T02:25:29'
supersedes: []
sources:
- papers/2110.14143.pdf
source_type: arxiv_paper
---

## Object Detection

**Object Detection** is a computer vision technique used to locate and classify objects within an image or scene. In the context of the [[Scene- and Object-Aware Transformer (SOAT)]], it serves as the second visual encoder, providing object-level features that the transformer aligns with natural language references.

### Description

Object detector used as the second visual encoder in [[Scene- and Object-Aware Transformer (SOAT)]], providing object-level features that the transformer aligns with textual references. It detects objects and aligns them to object references in instructions.

### Parameters

- **role**: Detects objects and aligns them to object references in instructions.

### Capabilities

- Matches object references (e.g., "green chairs").
- Enables better performance on instructions with many object references.

### Relationships

- **part_of** [[Scene- and Object-Aware Transformer (SOAT)]]
- **used_with** [[Scene Classification Network]] ⚠️
- **depends_on** visual input (images or video frames)
- **implements** object-level visual encoding for language grounding

### Usage Notes

This object detector is specifically tuned to work alongside a [[scene classification network]] ⚠️ within the SOAT architecture. Its strength lies in resolving ambiguous or multiple references in language instructions, making it a key component for [[Embodied AI]] systems that follow natural language commands.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Object Detection` --[[related_to]] ⚠️--> `Embodied AI`
