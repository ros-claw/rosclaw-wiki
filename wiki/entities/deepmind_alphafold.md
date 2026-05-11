---
id: deepmind_alphafold
type: entity
tags: [protein-folding, deep-learning, biology, alphafold, deepmind]
confidence: 0.95
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/alphafold_casp13
  - https://www.nature.com/articles/s41586-019-1923-7
---

# AlphaFold

AlphaFold is a deep learning system developed by [[DeepMind]] for predicting protein 3D structures from amino acid sequences. It achieved near-experimental accuracy at the CASP13 competition (2018), marking a significant breakthrough in computational biology.

## Architecture

AlphaFold uses a deep [[evolutionary_features|evolutionary]] and [[physical_constraints|physical]] approach:

- **MSA (Multiple Sequence Alignment)**: Input sequences are aligned with evolutionary relatives
- **Distogram Prediction**: Predicts probability distributions over residue-residue distances
- **Structure Module**: Iteratively refines 3D coordinates using [[attention_mechanism|attention]] layers

## Key Components

| Module | Description |
|--------|-------------|
| Input Embedder | Encodes MSA and pair representations |
| Evoformer | Processes evolutionary couplings via [[transformer|transformer]] blocks |
| Structure Module | Outputs 3D backbone coordinates with side-chain predictions |

## Impact

AlphaFold has been applied to:
- Drug discovery and [[molecular_dynamics|molecular dynamics]] simulations
- Understanding [[genetic_disease|genetic diseases]] through structure-function relationships
- Engineering novel [[enzyme_design|enzymes]] and proteins

## Relationship to Embodied AI

While primarily a computational biology tool, AlphaFold's architecture innovations — particularly its use of [[attention_mechanism|attention]] for spatial reasoning and iterative refinement — have influenced robotic perception systems that reason about 3D structure from partial observations.

## See Also

- [[deepmind_enformer|Enformer]] — Gene expression prediction from DNA sequence
- [[protein_structure_prediction|Protein Structure Prediction]]
- [[attention_mechanism|Attention Mechanism]]
