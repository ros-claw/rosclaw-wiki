---
id: imitation_learning
title: Imitation Learning
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-30T01:58:37'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2210.03112.pdf
- papers/1806.00047.pdf
source_type: arxiv_paper
---

# Imitation Learning

**Imitation Learning** is a machine learning paradigm in which an agent learns to perform a task by mimicking demonstrations provided by an expert, often using datasets of state-action pairs, rather than relying solely on reward signals (as in reinforcement learning). In the context of embodied AI and robotics, imitation learning enables the transfer of sensorimotor policies from human or synthetic demonstrations to physical or simulated agents.

## Definition

A paradigm where an agent learns a policy by imitating an expert's behavior, often using datasets of state-action pairs. The agent is trained to replicate the expert's actions given the observed states, a process commonly known as Behavioral Cloning ⚠️ ⚠️ when applied directly.

## Scale and Capabilities

The variant described in source `papers/2210.03112.pdf` is designed for **large-scale** training, while the foundational concepts in `papers/1806.00047.pdf` establish the general framework. Key capabilities include:

- Training transformer agents ⚠️ efficiently on massive demonstration datasets.
- Leveraging synthetic data ⚠️ at scale to generate diverse, high-quality instruction-trajectory pairs, reducing the need for expensive human teleoperation.
- Learning control policies directly from example trajectories, enabling transfer to real-world tasks.

## Relationships

- **used_for**: Imitation learning is directly used to train agents (e.g., transformer-based policies) through supervised learning over demonstration pairs.
- **implements**: This approach implements a supervised learning objective over demonstration pairs, contrasted with reinforcement learning methods which require online interaction and reward shaping.
- **used_by**: Grounded Semantic Mapping Network (GSMN) employs imitation learning to train its policy from expert demonstrations.

## Role in the Method

In the large-scale work (2210.03112), imitation learning is employed to train a simple transformer agent on **4.2 million synthetic instruction-trajectory pairs**. The agent, trained via this method, outperforms comparable RL agents ⚠️ trained from scratch, demonstrating that imitation learning with large, synthetic datasets can provide a strong prior for behavior. More generally, imitation learning serves as the foundation for many robot learning pipelines, including GSMN.

## Related Concepts

- Behavioral Cloning ⚠️ ⚠️
- Inverse Reinforcement Learning ⚠️
- Observation Space ⚠️
- Action Space ⚠️
- Sim-to-Real Transfer
- Grounded Semantic Mapping Network ⚠️

## Sources

- Paper: [papers/1806.00047.pdf](papers/1806.00047.pdf)
- Paper: [papers/2210.03112.pdf](papers/2210.03112.pdf)