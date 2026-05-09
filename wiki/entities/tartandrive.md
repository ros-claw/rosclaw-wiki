---
id: tartandrive
title: TartanDrive
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:33:12'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

# TartanDrive

TartanDrive is a large-scale, off-road driving dataset and benchmark designed for autonomous navigation research. It is part of the broader [[Navigation datasets]] ⚠️ ⚠️ collection and has been used as an unseen out-of-distribution test set to evaluate zero-shot generalization of the [[UniWM]] world model.

## Overview

TartanDrive provides multimodal sensor data (e.g., stereo imagery, LiDAR, IMU, and vehicle state) collected across diverse off-road terrains. In the ROSClaw knowledge base, it serves as a **benchmark dataset** for measuring how well learned models transfer to novel environments without fine-tuning. It is the unseen dataset on which UniWM demonstrated zero-shot generalization capabilities.

## Relationships

- **part\_of**: [[Navigation datasets]] ⚠️ ⚠️
- **used\_by**: [[UniWM]] — the dataset serves as an out-of-distribution evaluation target for the UniWM world model’s zero-shot capabilities.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `TartanDrive` --[[uses]] ⚠️--> `UniWM`

---

*Source: arxiv paper 2510.08713.pdf*