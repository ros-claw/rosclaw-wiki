---
id: mtu3d_move_to_understand_3d
title: MTU3D (Move to Understand 3D)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:57:20'
last_reinforced: '2026-04-29T20:57:20'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

## MTU3D (Move to Understand 3D)

**Type**: Algorithm  
**Category**: Vision-Language Navigation / Active Perception  

**Overview**  
MTU3D is a unified framework that bridges visual grounding and exploration for [[Embodied Navigation]]. It constructs [[spatial memory]] ⚠️ online from [[RGB-D frames]], jointly optimizes [[object grounding]] ⚠️ and frontier selection, and learns end-to-end trajectories via pre-training on large-scale data. By integrating active perception with [[3D Vision-Language Learning]], MTU3D enables embodied agents to effectively explore and understand their environment using categories, language descriptions, and reference images.

### Input Modalities & Training Data

**Parameters**:
- **Input modalities**:
  - [[RGB-D frames]]
  - [[Categories (object classes)]] ⚠️
  - [[Language descriptions]] ⚠️
  - [[Reference images]] ⚠️
- **Training data**: Million diverse trajectories from simulated and real-world RGB-D sequences.

### Capabilities

- Integrates active perception with 3D vision-language learning.
- Enables embodied agents to effectively explore and understand the environment.
- Navigates using **categories**, **language descriptions**, and **reference images**.
- Constructs spatial memory online from RGB-D frames.
- Jointly optimizes object grounding and frontier selection.
- Learns end-to-end trajectories via pre-training on large-scale data.

### Performance Benchmarks

MTU3D outperforms state-of-the-art methods on multiple benchmarks:

| Benchmark                 | Improvement (Success Rate) |
|---------------------------|----------------------------|
| HM3D-OVON                 | +14%                       |
| GOAT-Bench                | +23%                       |
| SG3D                      | +9%                        |
| A-EQA                     | +2%                        |

### Relationships

**uses**:
- [[Online query-based representation learning]]
- [[Unified objective for grounding and exploration]] ⚠️
- [[End-to-end trajectory learning]]
- [[Vision-Language-Exploration pre-training]]

**depends_on**:
- [[3D Vision-Language models]] ⚠️
- [[Spatial memory construction from RGB-D frames]]

### Further Reading

- [[RGB-D frames]]
- [[Embodied AI]]
- [[Object grounding in 3D scenes]] ⚠️
- [[Online representation learning for navigation]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MTU3D (Move to Understand 3D)` --[[extends]] ⚠️ ⚠️ ⚠️--> `Online query-based representation learning`
- `MTU3D (Move to Understand 3D)` --[[extends]] ⚠️ ⚠️ ⚠️--> `End-to-end trajectory learning`
- `MTU3D (Move to Understand 3D)` --[[extends]] ⚠️ ⚠️ ⚠️--> `Vision-Language-Exploration pre-training`
- `MTU3D (Move to Understand 3D)` --[[based_on]] ⚠️ ⚠️--> `Spatial memory construction from RGB-D frames`
- `MTU3D (Move to Understand 3D)` --[[based_on]] ⚠️ ⚠️--> `Embodied AI`
