---
id: unitree_b2
title: Unitree B2
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:35:41'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# Unitree B2

**Unitree B2** is a heavy‑duty quadruped robot platform developed by **Unitree Robotics** (manufacturer: Unitree). As a **legged robot**, it is designed for agile locomotion and payload‑heavy tasks, commonly used in research and industrial applications requiring robust outdoor mobility.

## Parameters

- **Robot Type:** Legged robot (quadruped)
- **Manufacturer:** Unitree Robotics
- **Platform Compatibility:** [[LOVON]] framework (plug‑and‑play)

## Capabilities

- **Long‑range object navigation in dynamic environments** – when integrated with the [[LOVON]] planning framework, the B2 becomes capable of reliably navigating complex, changing scenes over extended distances.
- **Open‑vocabulary object navigation** – the B2 served as a test platform for LOVON’s open‑vocabulary navigation experiments, demonstrating plug‑and‑play integration.

## Relationships

- `uses` → [[LOVON]] – the B2 acts as the mobile base for LOVON’s long‑range navigation policies, leveraging its high torque output and terrain adaptability. It was used in all LOVON experiments.

## Notes

This page is based on the source `papers/2507.06747.pdf` (arXiv preprint discussing LOVON deployment on the B2 platform). For detailed locomotion specifications, manufacturer‑provided parameters should be consulted.