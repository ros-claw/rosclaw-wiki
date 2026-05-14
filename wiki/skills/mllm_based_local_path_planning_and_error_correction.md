---
id: mllm_based_local_path_planning_and_error_correction
title: MLLM-based Local Path Planning and Error Correction
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T00:42:23'
last_reinforced: '2026-04-30T00:42:23'
supersedes: []
sources:
- papers/2509.20499.pdf
source_type: arxiv_paper
---

## MLLM-based Local Path Planning and Error Correction

**Definition**:  
MLLM-based Local Path Planning and Error Correction is a **skill** that uses a Multimodal Large Language Model (MLLM) to select navigable waypoints and correct errors during robot navigation. It operates over a Topological Graph with Visitation Records, reasoning about spatial structure and past visits to choose robust low-level actions.

### Parameters

| Input                                           | Output                                  |
|-------------------------------------------------|-----------------------------------------|
| Topological graph, visitation records, abstract waypoints | Selected next waypoint and low-level actions |

### Capabilities

- Reasons over a spatial graph to choose navigable routes.
- Detects and corrects navigation errors by reconsidering waypoint choices.
- Handles dead‑ends and loops using visitation history.

### Procedure

1. Receive candidate waypoints from the predictor.  
2. Update the topological graph with new nodes.  
3. Construct a prompt that includes graph structure and visitation counts.  
4. Query the MLLM to select the next waypoint.  
5. Execute movement toward that waypoint.  
6. If progress stalls or a violation is detected, the MLLM re‑plans via local adjustment.

### Relationships

- **depends_on**  
  - Topological Graph with Visitation Records  
  - Multimodal Large Language Model (MLLM)  

- **part_of**  
  - TopoGraph-and-VisitInfo-Aware Prompting

### Sources

- arXiv paper 2509.20499 – *"Visually guided local path planning and error correction via topological graph and visitation history"*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MLLM-based Local Path Planning and Error Correction` --uses ⚠️ ⚠️--> `Multimodal Large Language Model (MLLM)`
- `MLLM-based Local Path Planning and Error Correction` --uses ⚠️ ⚠️--> `TopoGraph-and-VisitInfo-Aware Prompting`
**Pending review:**
- `MLLM-based Local Path Planning and Error Correction` --related_to ⚠️--> `Topological Graph with Visitation Records` _(wikilink)_
