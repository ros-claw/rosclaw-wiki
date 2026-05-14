---
id: deepmind_learning_to_simulate
type: algorithm
tags: [learned-simulation, particle-based-methods, graph-networks, deepmind]
confidence: 0.88
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/learning_to_simulate
  - https://arxiv.org/abs/2002.09405
---

# Learning to Simulate

Learning to Simulate (L2S) is a particle-based learned simulator that uses [[graph_neural_network|Graph Networks]] to model complex physical phenomena including fluids, sand, and deformable materials at particle resolution.

## Core Approach

The method represents physical systems as particles with state features (position, velocity, material type) and learns to predict next-state dynamics:

```
Particle State_t → Graph Network → Particle State_{t+1}
```

### Graph Construction

- **Nodes**: Individual particles with type embeddings (water, sand, rigid, etc.)
- **Edges**: Radial connectivity within a neighborhood radius
- **Global features**: System-level parameters like gravity

## Advantages over Mesh-Based Methods

| Feature | Mesh-Based | Particle-Based (L2S) |
|---------|-----------|---------------------|
| Topology changes | Difficult (remeshing needed) | Natural (particles move freely) |
| Fracture/splitting | Complex | Automatic |
| Multi-material | Separate meshes | Single particle system |
| Memory | Mesh-dependent | Proportional to particles |

## Simulated Phenomena

The framework has been demonstrated on:
- **Water**: Surface tension, splashing, mixing
- **Sand**: Granular flow, pile formation, avalanches
- **Goop**: Viscoelastic materials, stretching and tearing
- **Multi-material**: Water-sand interactions, solid-fluid coupling

## Robotics Applications

- **Granular material manipulation**: Scooping, pouring, digging
- **Fluid tasks**: Pouring, stirring, liquid transfer
- **Deformable objects**: Folding cloth, manipulating bags
- **Real-time planning**: Fast rollouts for [[model_predictive_control|MPC]]

## Training Data

L2S is trained on ground-truth trajectories from traditional physics engines (MuJoCo, NVIDIA Flex), learning to approximate the dynamics with orders of magnitude speedup.

## See Also

- [[deepmind_meshgraphnets|MeshGraphNets]] — Mesh-based learned simulation
- [[graph_neural_network|Graph Neural Networks]]
- Differentiable Simulation
- Particle-Based Methods
