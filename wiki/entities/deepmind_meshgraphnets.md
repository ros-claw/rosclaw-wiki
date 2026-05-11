---
id: deepmind_meshgraphnets
type: algorithm
tags: [graph-neural-networks, physics-simulation, mesh-based-methods, deepmind]
confidence: 0.90
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/meshgraphnets
  - https://arxiv.org/abs/2010.03409
---

# MeshGraphNets

MeshGraphNets is a framework for learning mesh-based simulations using [[graph_neural_network|Graph Neural Networks (GNNs)]]. It enables fast, differentiable surrogate models for physics simulations that traditionally require expensive numerical solvers.

## Architecture

MeshGraphNets operates directly on unstructured meshes:

1. **Graph Construction**: Mesh vertices become nodes, edges connect adjacent mesh elements
2. **Encoder**: Node and edge features are embedded into latent representations
3. **Message Passing**: Multiple rounds of edge → node → edge updates propagate information
4. **Decoder**: Node embeddings predict next-state quantities (velocity, pressure, etc.)

## Key Innovation

Unlike prior neural physics simulators that required regular grids, MeshGraphNets works on arbitrary unstructured meshes, making it applicable to:

- **Fluid dynamics** on complex geometries
- **Structural mechanics** with irregular materials
- **Cloth simulation** with adaptive mesh resolution

## Performance

| Simulator | Speedup vs Ground Truth |
|-----------|------------------------|
| Water wave | 100-1000x |
| Airfoil (CFD) | 50-200x |
| Structural deformation | 100-500x |

## Relevance to Robotics

MeshGraphNets has direct applications in embodied intelligence:

- **Deformable object manipulation**: Real-time simulation of cloth, bags, and soft materials for planning
- **Fluid interaction**: Robots pouring liquids or operating in water
- **Sim-to-real transfer**: Fast differentiable simulators enable [[domain_randomization|domain randomization]] at scale
- **Model-based RL**: Learned physics models for planning and control

## Comparison with Traditional Methods

| Aspect | Traditional FEM/CFD | MeshGraphNets |
|--------|-------------------|---------------|
| Speed | Minutes/hours per frame | Milliseconds |
| Differentiability | No (or adjoint methods) | Yes (autodiff) |
| Mesh flexibility | Requires expertise | Learns adaptively |
| Accuracy | High (convergent) | Good (data-limited) |

## See Also

- [[deepmind_learning_to_simulate|Learning to Simulate]]
- [[graph_neural_network|Graph Neural Networks]]
- [[differentiable_physics|Differentiable Physics]]
- [[simulation|Physics Simulation for Robotics]]
