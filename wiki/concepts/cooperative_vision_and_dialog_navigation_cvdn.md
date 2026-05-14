---
id: cooperative_vision_and_dialog_navigation_cvdn
title: Cooperative Vision-and-Dialog Navigation (CVDN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:22:21'
last_reinforced: '2026-04-29T21:22:21'
supersedes: []
sources:
- papers/1907.04957.pdf
source_type: arxiv_paper
---

# Cooperative Vision-and-Dialog Navigation (CVDN)

**Type:** Concept  
**Source:** arxiv_paper ⚠️ — 1907.04957

## Overview

Cooperative Vision-and-Dialog Navigation (CVDN) is a benchmark and dataset for studying how agents can navigate indoor environments through natural language dialog. The CVDN dataset contains over 2,000 embodied, human-human dialogs recorded in photorealistic simulated home environments. In each dialog, a **Navigator** (the agent) asks questions to an **Oracle ⚠️** (a human with access to the optimal path and full environment knowledge), enabling the agent to infer actions toward a goal destination. This setup provides a realistic testbed for cooperative human-robot navigation ⚠️.

## Task Definition

The core task defined by CVDN is **Navigation from Dialog History**. Given a target object (e.g., "find the red cup on the kitchen counter") and the full dialog history exchanged between Navigator and Oracle, an agent must infer a sequence of navigation actions that will bring it to the goal location. The agent never receives direct visual feedback of the goal; all spatial reasoning must be done through the dialog interactions.

## Dataset Details

- **Size**: Over 2,000 dialogs  
- **Environment**: Photorealistic, simulated home environments (based on Matterport3D ⚠️ datasets)  
- **Roles**:  
  - *Navigator*: Asks questions to gather spatial information and navigates step-by-step.  
  - *Oracle*: Has access to the shortest path and the environment model; answers navigator queries truthfully.  
- **Data collection**: Human participants played both roles remotely, generating natural, unscripted dialogs.

## Capabilities

- Enables training of agents that can navigate using natural language dialog ⚠️  
- Provides a benchmark for cooperative human-robot navigation in unfamiliar environments  
- Supports evaluation of dialog-based spatial reasoning and grounding

## Relationships

- **CVDN** uses human-human dialogs ⚠️ for training data  
- **CVDN** uses shortest path planning ⚠️ for oracles  
- **CVDN** depends on photorealistic simulation ⚠️ ⚠️ for environment fidelity  
- **CVDN** implements the Navigation from Dialog History task  
- Related to Embodied Question Answering ⚠️ (EQA) and Vision-and-Language Navigation (VLN) but with a cooperative dialog element

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Cooperative Vision-and-Dialog Navigation (CVDN)` --related_to ⚠️--> `Vision-and-Language Navigation`
