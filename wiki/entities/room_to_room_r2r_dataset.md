---
id: room_to_room_r2r_dataset
title: Room-to-Room (R2R) dataset
type: entity
tags: []
confidence: 1.0
created_at: '2026-04-29T21:11:25'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2308.12587.pdf
- papers/2305.14268.pdf
- papers/2304.04907.pdf
- papers/2305.11918.pdf
- papers/1905.12255.pdf
source_type: arxiv_paper
---

# Room-to-Room (R2R) Dataset

The **Room-to-Room (R2R)** dataset provides paired navigation instructions and paths in real-world indoor environments (Matterport3D reconstructions), widely used for evaluating Vision-and-Language Navigation (VLN) ⚠️ agents. It is a core component of the Vision-and-Language Navigation benchmark suite ⚠️ ⚠️ and a central benchmark in vision-and-language navigation research.

## Overview

R2R was introduced to evaluate an agent’s ability to follow descriptive instructions in continuous, visually rich environments. Each instruction is a sequence of navigational actions (e.g., "go up the stairs, turn left, enter the bedroom"), grounded in a real-world 3D scene. The dataset supports both route-following and room-targeting tasks.

## Key Characteristics

- **Source environments**: 90 buildings from Matterport3D ⚠️ ⚠️, covering 10,800 panoramic viewpoints. The environments are simulated rooms within Matterport3D.
- **Instructions**: Approximately 7,200 human-written navigation instructions, each describing a full path of 2–12 steps. The instruction style is natural language.
- **Splits**: Standard train/val/val_unseen/test splits, with "unseen" environments to test generalization. The **val-unseen** split is specifically used to measure an agent's ability to generalize to novel environments.
- **Task type**: Goal-oriented, instruction-following navigation under discrete or continuous action spaces.

## Limitations

A key limitation of the R2R dataset is that its existing paths are **direct-to-goal shortest paths**, which do not adequately test **instruction following** because they minimize deviation and thus conflate goal completion with route adherence. The dataset is better suited for goal-completion metrics than for evaluating fine-grained instruction fidelity. This observation motivated the creation of the Room-for-Room (R4R) ⚠️ ⚠️ ⚠️ ⚠️ dataset, which concatenates multiple R2R paths to yield longer, more circuitous trajectories that better differentiate agents that genuinely follow instructions from those that merely find the goal.

## VLN Evaluation

The R2R dataset provides navigation instructions and trajectories in real-world environments. The **val-unseen** split tests generalization to new environments and is the most challenging evaluation setting. Recent work has achieved a **1.32% absolute improvement in success rate** when using the MPM (Multi-Perspective Matching) method, demonstrating the benchmark's sensitivity to architectural innovations.

Despite its predominance, the R2R benchmark has been criticized for its reliance on shortest‑path trajectories, which can mask failures in instruction following. Researchers now often supplement R2R results with evaluations on R4R and Room-Across-Room (RxR) to obtain a fuller picture of agent capability.

## Usage

The R2R dataset is the primary benchmark for VLN ⚠️ models. It is used to train and evaluate agents that combine language understanding, visual perception, and sequential decision-making. Common approaches include Transformer-based VLN models ⚠️, reinforcement learning, and imitation learning with attention mechanisms. Notably, the **Progress-Aware Spatio-Temporal Transformer Speaker (PASTS)** model uses the R2R dataset as a standard evaluation benchmark. Results on R2R, especially on the val-unseen and test splits, are widely reported as standard metrics in the field. It is also used by the VLN-SIG (Vision-and-Language Navigation Special Interest Group) as a standard evaluation tool and remains the most commonly reported benchmark in VLN research.

## Related Datasets

- Room-Across-Room (RxR): Extended version with multi-lingual instructions and finer-grained annotations.
- Room-for-Room (R4R) ⚠️ ⚠️ ⚠️ ⚠️: A variant derived from R2R by concatenating existing short paths to form longer, more complex trajectories. R4R was created to provide a more challenging benchmark for evaluating **instruction fidelity** in VLN. It enables evaluation using the **Coverage weighted by Length Score (CLS)** metric, and experiments have shown that agents rewarded for instruction fidelity (e.g., following the exact path) outperform those focused solely on goal completion. **R4R supersedes R2R for instruction-fidelity evaluation** because its longer, non‑shortest‑path trajectories better distinguish genuine instruction following from goal finding.
- Touchdown ⚠️: Navigation in street-view imagery.
- CVDN: Collaborative VLN via dialog.

## Relationship Annotations

- **depends_on**: Matterport3D ⚠️ ⚠️ for visual environments.
- **part_of**: Vision-and-Language Navigation benchmark suite ⚠️ ⚠️.
- **superseded_by**: Room-for-Room (R4R) ⚠️ ⚠️ ⚠️ ⚠️ (for instruction fidelity evaluation).
- **used_by**: VLN agents ⚠️, Embodied AI benchmarks, VLN-SIG, Vision-and-Language Navigation, PASTS (Progress-Aware Spatio-Temporal Transformer Speaker), VLN research ⚠️.
- **related_to**: Instruction following ⚠️, Visual grounding, Navigation policy learning ⚠️, Room-for-Room (R4R) ⚠️ ⚠️ ⚠️ ⚠️, Room-across-Room (RxR).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room-to-Room (R2R) dataset` --related_to ⚠️--> `Embodied AI`