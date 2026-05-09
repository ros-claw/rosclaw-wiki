---
id: avdn_dataset
title: AVDN Dataset
type: concept
tags: []
confidence: 0.9
created_at: '2026-04-29T21:09:20'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2205.12219.pdf
- papers/2308.12587.pdf
- papers/2304.04907.pdf
source_type: arxiv_paper
---

# CVDN Dataset

The **CVDN Dataset** (Cooperative Vision-and-Dialog Navigation) is a large-scale benchmark for [[Vision-and-Dialog Navigation]], collected through human-human asynchronous dialogs between commanders and followers in a continuous photorealistic simulation. It provides over 3k recorded trajectories with annotations including the follower's attention on visual observations, enabling the training and evaluation of models that perform goal-oriented navigation guided by natural language dialog. The dataset captures human-human dialogues for navigation, testing agents in interactive settings, and serves as a key benchmark for dialog-enabled [[Vision-and-Language Navigation]] (VLN).

## Parameters

- **Type**: Dataset
- **Task**: Cooperative navigation with dialogue (vision-and-language navigation with dialogue instructions)
- **Instruction type**: Dialogue-based
- **Size**: Over 3k recorded trajectories.
- **Collection paradigm**: Human-human asynchronous dialogs between commanders (giving instructions) and followers (executing navigation in simulation).
- **Annotations**: Includes the follower's attention on visual observations, capturing where the follower looked during the task.
- **Environment**: Simulated indoor (continuous photorealistic simulation such as Matterport3D), providing a high-fidelity visual setting for embodied cooperative navigation.

## Capabilities

- Train models for cooperative navigation from dialog, leveraging both the linguistic exchanges and visual attention.
- Evaluate vision-and-dialog navigation performance on a standardized benchmark with diverse trajectories and interaction patterns.
- **Benchmark for dialog-enabled VLN**: The dataset provides a standard evaluation framework for agents that must interpret and follow dialog-based navigation instructions.

## Relationships

- **Part of**: [[Vision-and-Dialog Navigation]] — the dataset is a core component of this research area, enabling reproducible experiments in human-robot dialog for navigation.
- **Used by**: [[VLN-SIG]], [[Vision-and-Language Navigation]] — the dataset is employed in these research communities to benchmark and advance cooperative navigation agents.
- **Contrasts with**: [[AVDN Dataset]] — the AVDN dataset focuses on aerial (drone) navigation, whereas CVDN covers ground-level cooperative navigation in indoor environments. Both use dialog but differ in embodiment and simulation.

### 待核实冲突

- **Previous title**: This page was originally titled *AVDN Dataset*, which refers to a separate, aerial-based dataset. The source paper (arXiv:2308.12587) is specifically the *CVDN* benchmark. The parameters (size, collection paradigm, annotations) match CVDN; the aerial context and the relationship to [[HAA-Transformer]] likely belong to the AVDN dataset and are removed pending verification. A separate page for AVDN should be created or linked.

## See Also

- [[Vision-and-Dialog Navigation]] — the broader concept of navigation guided by human-robot dialog.
- [[Embodied AI]] — the field in which this dataset sits.
- [[AVDN Dataset]] — related aerial benchmark (note: may need creation).
- [[VLN-SIG]] — research group that uses this dataset.
- [[Vision-and-Language Navigation]] — broader VLN task family.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `AVDN Dataset` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `AVDN Dataset` --[[related_to]] ⚠️ ⚠️--> `HAA-Transformer` _(wikilink)_