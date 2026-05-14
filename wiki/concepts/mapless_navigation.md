---
id: mapless_navigation
title: Mapless Navigation
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:50:47'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2503.03921.pdf
- papers/2511.06840.pdf
source_type: arxiv_paper
---

### Mapless Navigation

**Type:** concept  

Mapless navigation refers to the task of navigating an environment **without relying on pre-existing maps**. The agent uses only onboard sensors and learned representations to perceive, plan, and move through unknown or changing spaces. This paradigm is essential for long‑term autonomy in unstructured or GPS‑denied environments.

---

**Capabilities**  
- Navigation without pre‑built maps  
- Scalable to kilometer‑scale missions  
- Navigation without metric maps **or depth sensors** (subject to conflicting evidence – see below)  

---

**Advantage**  
Reduces hardware requirements and pre‑mapping efforts, enabling deployment on platforms that lack expensive depth sensors or prior environmental surveys.

---

**Relationships**  
- The approach is addressed by CREStE, a system that enables robust mapless navigation over long distances.  
- Mapless Navigation is related to Zero-shot navigation, as both aim to operate without prior exposure to the environment.

---

**Description**  
Mapless navigation replaces traditional map‑based pipelines with sensor‑driven policies. It often combines visual odometry, depth estimation, and learned controllers (e.g., reinforcement learning or end‑to‑end imitation learning) to navigate from one location to another without a global map. The ability to scale to kilometer‑scale missions demands efficient representation learning and memory management, making it a key challenge in mobile robotics.

---

### 待核实冲突

The following discrepancy was noted when integrating new source facts:

- **Source claim (parameters):** `no_map: true`, `no_depth_sensor: false` — suggesting that the system **does** use a depth sensor.  
- **Source claim (capabilities):** “navigation without metric maps or depth sensors” — suggesting that the system **does not** use a depth sensor.  

These two assertions are contradictory. The user is advised to consult the original paper (`data/raw/papers/2511.06840.pdf`) to resolve the intended meaning. Both interpretations are recorded here for future reconciliation.

---

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Mapless Navigation` --related_to ⚠️ ⚠️--> `CREStE` _(wikilink)_
- `Mapless Navigation` --related_to ⚠️ ⚠️--> `Zero-shot navigation` _(wikilink)_