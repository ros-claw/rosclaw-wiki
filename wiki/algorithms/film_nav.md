---
id: film_nav
title: FiLM-Nav
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:37:18'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2509.16445.pdf
- papers/2509.16445.json
source_type: arxiv_paper
---

# FiLM-Nav

**FiLM-Nav** is an algorithm that fine-tunes a pre-trained Vision-Language Model (VLM) directly as a navigation policy, using raw visual trajectory history and a natural language goal as input. It achieves state-of-the-art performance on object navigation benchmarks by leveraging a diverse mixture of simulated embodied experiences.

---

## Approach

FiLM-Nav treats navigation as a visual-language mapping problem. The policy receives:

- **Raw visual trajectory history** — a sequence of past observations from the agent's camera.
- **Navigation goal** — a natural language description of the target object or location.

The pre-trained VLM is fine-tuned end-to-end on this input, producing agent actions directly. No separate mapping, planning, or explicit scene representation is used. The learned policy implicitly learns to select the next best exploration frontier based on visual context and the goal, enabling efficient coverage of complex environments. The method is therefore described as a **Fine-tuned Language Model for Navigation**.

## Capabilities

- **Open-vocabulary navigation** – can navigate to novel object categories not seen during training.
- **Navigate complex environments** – moves through cluttered, multi-room spaces while reasoning about obstacles and pathways.
- **Locate objects described in free-form language** – understands natural language descriptions such as "find the red mug on the kitchen counter."
- **Select next best exploration frontier** – integrates visual history and goal to decide where to move next, effectively balancing exploration and exploitation.
- **Generalize to unseen object categories** – performs zero-shot transfer to object types not present in the training mixture.
- Achieves **state-of-the-art SPL and success rate** on HM3D ObjectNav ⚠️.
- Achieves **state-of-the-art SPL** on HM3D-OVON.
- Demonstrates **efficient and generalizable semantic navigation** in simulated environments.

## Training Data Mixture

FiLM-Nav is trained on a diverse combination of tasks and datasets:

- ObjectNav
- OVON (Open-Vocabulary Object Navigation)
- ImageNav
- Spatial reasoning task (synthetic)

This mixture, combining ObjectNav, OVON, ImageNav, and auxiliary spatial reasoning, enables the policy to learn robust goal-conditioned navigation behaviors that generalize beyond any single task. Fine-tuning on this diverse data is essential to the method's success. The simulated experiences are rendered in environments from the HM3D dataset, which provides the photorealistic 3D scenes used for training and evaluation.

## Relationships

- `uses` → Vision-Language Model (VLM)  
- `depends_on` → Fine-tuning ⚠️ (end-to-end from simulated trajectory-goal pairs)  
- `depends_on` → Simulated embodied experience ⚠️ (rendered trajectory-goal pairs)  
- `depends_on` → HM3D dataset  
- `depends_on` → Diverse data mixture combining ObjectNav, OVON, ImageNav, auxiliary spatial reasoning  
- `implements` → Open-vocabulary navigation ⚠️

## Summary

FiLM-Nav fine-tunes a pre-trained Vision-Language Model (VLM) directly as a navigation policy, using a diverse mixture of simulated embodied tasks (ObjectNav, OVON, ImageNav, spatial reasoning). It achieves state-of-the-art performance on HM3D ObjectNav and HM3D-OVON benchmarks, demonstrating strong generalization.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `FiLM-Nav` --based_on ⚠️ ⚠️--> `Vision-Language Model (VLM)`
- `FiLM-Nav` --based_on ⚠️ ⚠️--> `HM3D-OVON`