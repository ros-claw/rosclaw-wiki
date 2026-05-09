---
id: led_baseline_model
title: LED Baseline Model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:56:52'
last_reinforced: '2026-04-30T02:56:52'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

## LED Baseline Model

The **LED Baseline Model** is a baseline algorithm for the task of **Localization from Embodied Dialog (LED)**. It processes a dialog history and first‑person visual observations to localize an Observer agent within a building, achieving 32.7% success within a 3‑meter radius on unseen buildings in the [[Where Are You? Dataset]].

### Capabilities

- Localizes the Observer agent from a recorded dialog history.
- Fuses information from both dialog turns and visual observations.
- Serves as a reference point for evaluating more sophisticated models on the LED task.

### Model Architecture

The exact architecture is not detailed in the original abstract, but the model was ablated to determine the relative importance of the dialog and visual modalities. This analysis justifies the use of both input streams in the LED task.

### Performance

Tested on the [[Where Are You? Dataset]], the baseline achieves **32.7% success** (within 3 meters of the ground‑truth location) on unseen buildings. This performance establishes a strong foundation for the LED task and provides a benchmark for future work.

### Dependencies

- **uses**:: [[Where Are You? Dataset]]
- **depends_on**:: [[dialog history]] ⚠️, [[visual observations]] ⚠️
- **task**:: [[Localization from Embodied Dialog]] ⚠️