---
id: localization_from_embodied_dialog_led
title: Localization from Embodied Dialog (LED)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:21:49'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

# Localization from Embodied Dialog (LED)

**Localization from Embodied Dialog (LED)** is the task of determining the physical location of an Observer (e.g., a robot or human) based solely on the history of a dialog. The goal is to predict the Observer's location within a radius of **3 meters** using conversational context that may include references to landmarks, directions, or spatial relationships described by participants. LED is one of three tasks defined on the Where Are You? Dataset (WAY), alongside other embodied dialog benchmarks.

## Task Definition

LED requires predicting the Observer's position given the dialog history. The model must infer location from natural language exchanges that occur while the Observer moves through an environment. The task is evaluated on unseen buildings, with a baseline model achieving **32.7% success** at identifying the Observer's location within 3m, compared to **70.4%** for human Locators.

## Capabilities

- Given a dialog history, LED predicts the Observer's location with a spatial accuracy of **3m** or better.
- The prediction relies on verbal cues and implicit spatial information embedded in the conversation, without requiring explicit sensor data or visual input during inference.
- The baseline model demonstrates the feasibility of the task, though a significant gap remains between automated performance (32.7% on unseen buildings) and human performance (70.4%).
- The model utilizes both dialog context and visual observations (first-person views and top-down maps) when available.

## Dependencies

LED **depends_on**:

- Embodied Dialog ⚠️ ⚠️ — the broader framework in which an agent engages in conversation while situated in a physical environment. LEDs build on the assumption that dialog carries spatial information embedded in natural language.
- Visual Dialog ⚠️ ⚠️ — because LED often uses visual grounding to link linguistic references to visual features. The dialog history typically originates from a visual dialog task where participants discuss images or video of the environment.
- **Dialog history** — the sequence of conversational turns between participants, which embeds spatial references.
- **First-person views** — egocentric visual observations that accompany the dialog, providing visual context for location disambiguation.
- **Top-down map** — a bird's-eye representation of the environment, used by baseline models to map linguistic spatial cues to candidate positions.

## Dataset

LED is defined as one of three tasks in the Where Are You? Dataset (WAY). The dataset provides dialog histories paired with first-person views, top-down maps, and ground-truth observer positions. The task is evaluated on held-out buildings to test generalization.

## Model and Ablations

The LED baseline model is a neural architecture that integrates dialog history, first-person visual features, and map-based spatial reasoning. Detailed ablation studies characterize dataset biases and the importance of each input modality. Key findings include:

- Visual observations (first-person views and top-down maps) significantly improve localization when combined with dialog.
- The dialog alone contains strong spatial cues, but performance degrades on unseen buildings without visual grounding.
- Model design choices (e.g., attention mechanisms, fusion strategies) have substantial impact on out-of-distribution generalization.

## Relationship Annotations

| Relationship | Target            | Description |
|--------------|-------------------|-------------|
| depends_on   | Embodied Dialog ⚠️ ⚠️  | LED is a sub-task within embodied dialog, requiring situated conversation. |
| depends_on   | Visual Dialog ⚠️ ⚠️    | Dialog history is generated in a visual dialog setting; spatial references are grounded in visual observations. |
| part_of      | Where Are You? Dataset | LED is one of three tasks defined on the WAY dataset. |
| uses         | Where Are You? Dataset | LED models are trained and evaluated on the WAY dataset. |

## References

- ArXiv paper "Localization from Embodied Dialog" (2011.08277) — defines the LED task, baseline model, ablations, and evaluation methodology on the WAY dataset.