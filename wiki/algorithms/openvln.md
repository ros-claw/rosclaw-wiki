---
id: openvln
title: OpenVLN
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:53:44'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

## OpenVLN

### Overview

**OpenVLN** is a data-efficient open-world aerial Vision-Language Navigation framework. It uses a reinforcement learning framework to fine-tune a Vision-Language Model (VLM) for UAV navigation tasks under limited training data. The method incorporates rule-based policies and a long-horizon planner that generates UAV actions via value-based rewards, enabling language-guided flight in complex aerial environments. Validation is conducted on the TravelUAV benchmark.

### Approach

OpenVLN reconfigures a Reinforcement Learning framework to optimize the VLM using rule-based policies under constrained data conditions. It introduces a long-horizon planner that dynamically synthesizes precise UAV actions through value-based rewards, enabling efficient exploration and trajectory generation.

### Training

The framework fine-tunes the VLM using rule-based policies within a reinforcement learning loop, achieving high data efficiency. The long-horizon planner leverages value-based rewards to generate action sequences, allowing the model to learn effectively from limited training examples.

### Performance

Evaluated on the TravelUAV benchmark with dataset scaling across diverse reward settings, OpenVLN achieves consistent gains over baseline methods:

- **Success Rate**: +4.34%
- **Oracle Success Rate**: +6.19%
- **Success weighted by Path Length (SPL)**: +4.07%

These improvements demonstrate the framework's ability to enhance long-horizon trajectory planning and language-guided flight.

### Capabilities

- Executes language-guided flight with limited training data
- Enhances long-horizon trajectory planning in complex aerial environments
- Enables open-world aerial Vision-Language Navigation
- Improves Success Rate by up to 4.34%, Oracle Success Rate by up to 6.19%, and SPL by up to 4.07%

### Parameters

| Parameter | Value |
|-----------|-------|
| Type | Reinforcement learning framework for fine-tuning vision-language models for UAV navigation |
| Data efficiency | Limited data constraints |
| Key components | Rule-based policies, long-horizon planner, value-based rewards |
| Fine-tuning method | Reinforcement Learning with rule-based policies |
| Trajectory planner | Long-horizon planner with value-based rewards |

### Relationships

- **Uses**: Vision-Language Model, Reinforcement Learning
- **Depends on**: TravelUAV benchmark
- **Implements**: Airborne Vision-Language Navigation ⚠️