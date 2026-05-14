---
id: lstm
title: LSTM
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:13:28'
last_reinforced: '2026-04-29T21:13:28'
supersedes: []
sources:
- papers/2305.11918.pdf
source_type: arxiv_paper
---

# LSTM

## Definition

Long Short-Term Memory (LSTM) is a type of recurrent neural network (RNN) architecture designed to model sequential data and capture long-range dependencies through a gated cell state mechanism. LSTMs mitigate the vanishing gradient problem of traditional RNNs by introducing input, forget, and output gates, allowing information to persist over many time steps. In the context of embodied AI and vision-and-language navigation (VLN), LSTM networks have been widely used as sequence encoders and decoders — particularly in **speaker models** that generate language descriptions from visual trajectories.

## Role in VLN

LSTM serves as a backbone for many **speaker models** in VLN, where the network takes a sequence of visual observations and actions and produces natural language instructions. These LSTM-based speakers learn to map a walk-through trajectory to a textual description, enabling data augmentation and instruction generation. Common formulations use an LSTM with attention over visual features, decoding tokens step-by-step.

## Performance Comparison

Recent work has shown that LSTM-based speakers can be outperformed by transformer-based alternatives. According to PASTS (Paper 2305.11918), the PASTS architecture achieves superior performance on speaker-conditioned VLN tasks compared to LSTM-based speakers. This suggests a trend towards replacing recurrent architectures with parallelizable, attention-based models for instruction generation in embodied navigation.

## Related Concepts

- PASTS – a transformer-based speaker architecture that outperforms LSTM-based approaches.
- Vision-Language Navigation (VLN) – the primary domain where LSTM speakers are applied.
- Recurrent Neural Network (RNN) ⚠️ – the broader family to which LSTM belongs.
- Sequence-to-Sequence Learning ⚠️ – the paradigm used by LSTM-based speakers.
- Transformer ⚠️ – the architecture that has supplanted LSTM in many speaker models.

## Relationship Annotations

- PASTS `outperforms` LSTM-based speakers (comparison)
- LSTM `is used_by` speaker models in Vision-Language Navigation (VLN) (used_by)
- LSTM `depends_on` Gated Recurrent Mechanisms ⚠️ (implicit)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `LSTM` --extends ⚠️--> `PASTS`
