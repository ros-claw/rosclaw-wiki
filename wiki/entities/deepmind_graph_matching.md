---
id: deepmind_graph_matching
type: algorithm
tags: [graph-neural-networks, graph-matching, combinatorial-optimization, deepmind]
confidence: 0.88
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/graph_matching_networks
  - https://arxiv.org/abs/2012.08702
---

# Graph Matching Networks

Graph Matching Networks (GMNs) learn to compute similarity between graphs using a differentiable message-passing architecture, enabling applications in combinatorial optimization and graph alignment.

## Problem Formulation

Given two graphs G1 = (V1, E1) and G2 = (V2, E2), the goal is to learn a similarity function:

```
sim(G1, G2) = f_encoder(G1) ⊙ f_encoder(G2)
```

Where the encoder produces graph-level embeddings via iterative message passing.

## Architecture

### Cross-Graph Attention

Unlike standard [[graph_neural_network|GNNs]] that process each graph independently, GMNs introduce cross-graph attention:

- **Intra-graph propagation**: Standard message passing within each graph
- **Cross-graph attention**: Each node in G1 attends to all nodes in G2 (and vice versa)
- **Aggregation**: Node embeddings are pooled into graph-level representations

### Message Passing Equations

For node i in graph A at layer l:

```
m_i^A = Σ_j M(h_i^A, h_j^A, e_ij) + Σ_k M'(h_i^A, h_k^B)
```

Where the second sum is the cross-graph message from graph B.

## Applications

| Domain | Task |
|--------|------|
| Control | Learning control policies for combinatorial problems |
| Chemistry | Molecular similarity and reaction prediction |
| Scene Understanding | Matching object graphs across viewpoints |

## Relevance to Robotics

Graph matching is fundamental to:
- **Scene graph alignment**: Matching observed scene structures to known object configurations
- **Task planning**: Matching current world state graphs to goal state graphs
- **SLAM**: Place recognition via graph similarity in [[topological_mapping|topological maps]]

## See Also

- [[graph_neural_network|Graph Neural Networks]]
- [[attention_mechanism|Attention Mechanism]]
- [[deepmind_meshgraphnets|MeshGraphNets]] — Graph-based physics simulation
