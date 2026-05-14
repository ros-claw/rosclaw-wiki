---
id: deepmind_byol
type: algorithm
tags: [self-supervised-learning, representation-learning, computer-vision, contrastive-learning, deepmind]
confidence: 0.92
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/byol
  - https://arxiv.org/abs/2006.07733
---

# BYOL (Bootstrap Your Own Latent)

BYOL is a self-supervised learning algorithm for visual representation learning that achieves performance comparable to [[contrastive_learning|contrastive methods]] without requiring negative pairs.

## Core Idea

Unlike SimCLR or MoCo which rely on contrasting positive and negative samples, BYOL uses:

- **Online Network**: Produces predictions from augmented views
- **Target Network**: Generates regression targets via exponential moving average of online weights
- **Predictor Head**: Maps online representations to target representations

## Architecture

```
Augmented View 1 → Online Encoder → Online Predictor → Prediction
                                         ↑
Augmented View 2 → Target Encoder ──────┘
                     (EMA of Online)
```

## Key Insight

The method works because the predictor must learn to align representations across augmentations, effectively bootstrapping useful features without explicit negatives. The batch normalization layers play a crucial role in preventing collapse.

## Applications in Robotics

BYOL's representation learning is particularly valuable for [[embodied_ai|embodied AI]]:

- **Pre-training visual encoders** for downstream manipulation tasks
- **Domain adaptation** between simulation and real-world visual observations
- **Data efficiency** when labeled robot demonstration data is scarce

## Comparison with Related Methods

| Method | Negative Pairs | Batch Size Sensitivity | Performance |
|--------|---------------|----------------------|-------------|
| SimCLR | Yes | High | Strong |
| MoCo | Yes (queue) | Medium | Strong |
| BYOL | No | Low | Strong |
| SwAV | No (clustering) | Medium | Strong |

## See Also

- [[deepmind_curl|CURL]] — Contrastive unsupervised representations
- [[self_supervised_learning|Self-Supervised Learning]]
- Visual Representation Learning
