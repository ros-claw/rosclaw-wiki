---
id: deepmind_curl
type: algorithm
tags: [self-supervised-learning, reinforcement-learning, representation-learning, deepmind]
confidence: 0.85
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/curl
  - https://arxiv.org/abs/2004.04136
---

# CURL (Contrastive Unsupervised Representations for Reinforcement Learning)

CURL combines [[contrastive_learning|contrastive learning]] with [[reinforcement_learning|reinforcement learning]] to learn data-efficient visual representations for control tasks from pixels.

## Motivation

Standard RL from pixels (e.g., [[dqn|DQN]], [[sac|SAC]]) learns task-specific representations that:
- Require millions of environment steps
- Overfit to training environments
- Fail to transfer across tasks

CURL addresses this by pre-training visual representations using contrastive learning, then fine-tuning for control.

## Method

### Contrastive Objective

Given two augmented views of the same observation:
- **Query**: Augmented crop from current observation
- **Key**: Augmented crop from the same observation (different augmentation)

The model learns to maximize similarity between query-key pairs while minimizing similarity to other keys in a memory buffer.

### Architecture

```
Observation → Encoder → Projection Head → Contrastive Loss
                ↓
            Latent Representation → RL Policy/Value
```

## Key Results

| Environment | CURL Sample Efficiency vs Baseline |
|-------------|-----------------------------------|
| DeepMind Control Suite | 10-20x improvement |
| Atari | 2-5x improvement |

## Technical Details

- **Encoder**: Standard CNN (similar to [[resnet|ResNet]])
- **Projection**: MLP with 2-3 layers
- **Memory**: Momentum-encoded key encoder with queue
- **Augmentations**: Random crop, color jitter, grayscale

## Connection to Embodied AI

CURL is directly applicable to robotic visual learning:
- **Sample efficiency**: Critical for real-world robot data collection
- **Transfer**: Learned representations transfer across manipulation tasks
- **Sim-to-real**: Contrastive pre-training bridges the sim-to-real visual gap

## See Also

- [[deepmind_byol|BYOL]] — Self-supervised learning without negatives
- [[contrastive_learning|Contrastive Learning]]
- [[reinforcement_learning|Reinforcement Learning]]
- [[sim_to_real|Sim-to-Real Transfer]]
