---
id: scene_intuitive_agent
title: Scene-Intuitive Agent
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:12:16'
last_reinforced: '2026-04-30T02:12:16'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

# Scene-Intuitive Agent

The **Scene-Intuitive Agent** is a remote embodied visual grounding algorithm designed to navigate to a target object specified by a high-level instruction. It mimics the human intuitive understanding of visual environments and natural language, enabling agents to interpret complex spatial relationships and semantic cues. The agent is evaluated on the REVERIE task ⚠️ ⚠️ and relies on cross-modal alignment between visual scenes and language descriptions.

## Architecture and Training

The agent is trained in **2 stages**, each focusing on a distinct subtask:
- **Scene Grounding** – learning to associate visual scene context with global instruction semantics.
- **Object Grounding** – fine-grained alignment of local object features with specific noun phrases in an instruction.

The core action decoder is the Memory-Augmented Attentive Action Decoder, which combines an episodic memory buffer with cross-modal attention to decide navigation steps.

## Dependencies

- **Depends on**: Cross-modal pretraining ⚠️ to initialize visual and language encoders with aligned representations.
- **Uses**: REVERIE task ⚠️ ⚠️ (Remote Embodied Visual Referring Expression in Indoor Environments) as the benchmark for evaluation.
- **Uses**: Cross-modal alignment to fuse visual and linguistic features at multiple temporal scales.

## Capabilities

- Performs **remote embodied visual grounding** – the agent can understand instructions referring to objects not currently in view and navigate toward them.
- Executes **navigation to a target object** solely from a high-level natural language command.
- Demonstrates **human-intuitive understanding** of scenes and language, reducing the gap between raw sensor input and semantic comprehension.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Scene-Intuitive Agent` --extends ⚠️--> `Memory-Augmented Attentive Action Decoder`
- `Scene-Intuitive Agent` --based_on ⚠️--> `Cross-modal alignment`
