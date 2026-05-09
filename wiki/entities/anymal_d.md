---
id: anymal_d
title: ANYmal D
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:36:21'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

**ANYmal D** is a quadruped robot platform developed by [[ANYbotics]] ⚠️ ⚠️, used as a validation platform for agile locomotion policies. In the paper, it demonstrates robust generalization across real-world 3D scans for tasks like parkour and navigation over diverse unstructured terrains.

## Capabilities

- Agile locomotion and parkour
- Navigation over diverse unstructured terrains
- Robust generalization across real-world 3D scans

## Hardware

ANYmal D is a legged robot platform, manufactured by [[ANYbotics]] ⚠️ ⚠️, used for validation of the proposed agile locomotion policy. It relies on depth images as exteroceptive input for perception and terrain assessment.

## Deployment

The policy was deployed on the ANYmal D robot, demonstrating agility and robustness in complex environments through real-world trials. The deployment pipeline integrates the learned policy with the robot's onboard sensing and control stack.

## Relationships

- **Uses**: [[Multi-expert Distillation]], [[DAgger]], [[RL fine-tuning]] ⚠️, [[Depth Images as Exteroceptive Input]]
- **Depends on**: [[depth images]] ⚠️
- **Implements**: agile locomotion policy deployment on [[ANYmal D]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ANYmal D` --[[uses]] ⚠️ ⚠️--> `Multi-expert Distillation`
- `ANYmal D` --[[uses]] ⚠️ ⚠️--> `Depth Images as Exteroceptive Input`
- `ANYmal D` --[[implements]] ⚠️--> `Agile Locomotion Policy Deployment on ANYmal D`