---
id: unitree_h1_2
title: Unitree H1-2
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:36:25'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# Unitree H1-2

The **Unitree H1-2** is a bipedal humanoid robot platform developed by Unitree Robotics. It is an evolution of the [[Unitree H1]] ⚠️ series, designed for dynamic locomotion and manipulation tasks. The H1-2 features enhanced joint torque and control bandwidth, enabling it to operate in complex, unstructured environments.

## Parameters

- **Robot type**: Legged robot (bipedal)
- **Manufacturer**: [[Unitree Robotics]] ⚠️
- **Platform compatibility**: The H1-2 is a plug-and-play platform for the [[LOVON]] (Long-range Object Navigation) framework, serving as a direct testbed for open‑vocabulary navigation and manipulation.

## Capabilities

- **Long-range object navigation in dynamic environments** — When integrated with the [[LOVON]] framework, the H1-2 can navigate cluttered and changing spaces to autonomously approach and interact with distant objects. This capability combines robust locomotion with real-time semantic reasoning.
- **Test platform for LOVON open‑vocabulary object navigation** — The H1-2 has been used as a primary experimental platform to validate the LOVON architecture in real-world settings, demonstrating zero-shot generalization to new objects and environments.

## Relationships

- **uses** → [[LOVON]] (The H1-2 provides the physical embodiment for the LOVON framework, enabling long-range navigation and manipulation.)
- **used_in** → [[LOVON]] experiments (The H1-2 was deployed in all LOVON validation trials, serving as the mobile platform for evaluation.)

## Sources

- arxiv paper 2507.06747 (details the [[LOVON]] deployment on the Unitree H1-2)