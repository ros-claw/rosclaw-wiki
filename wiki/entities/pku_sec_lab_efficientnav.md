---
id: pku_sec_lab_efficientnav
title: PKU-SEC-Lab_EfficientNav
type: entity
tags:
- code_repository
- python
confidence: 0.7
sources:
- code/PKU-SEC-Lab_EfficientNav
source_type: official_manual
supersedes: []
---

# PKU-SEC-Lab_EfficientNav

**Source:** [https://github.com/facebookresearch/habitat-sim.git](https://github.com/facebookresearch/habitat-sim.git)
**Languages:** Python
## Installation
Assuming you have conda installed, let's prepare a conda env:
```
conda create -n habitat python=3.9 cmake=3.14.0
conda activate habitat
```
Install required packages:
```
pip install -r requirements.txt
```
Install habitat-sim:
```
git clone https://github.com/facebookresearch/habitat-sim.git
cd habitat-sim
conda install habitat-sim headless -c conda-forge -c aihabitat
```
Install habitat-lab:
``

## Relationships
- **Implements / Related to**: [[GRPO]]
- **Implements / Related to**: [[GRPO reinforcement learning]]
- **Implements / Related to**: [[Language-guided urban navigation]]
- **Implements / Related to**: [[Navigation from Dialog History]]
- **Implements / Related to**: [[Embodied 3D Occupancy Prediction]]

## See Also
- [[Code Repository]] ⚠️ — general code entity guidelines
- [[GRPO]]
- [[GRPO reinforcement learning]]
- [[Language-guided urban navigation]]
