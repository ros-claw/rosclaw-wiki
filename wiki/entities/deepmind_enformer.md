---
id: deepmind_enformer
type: algorithm
tags: [genomics, gene-regulation, transformer, dna-sequence, deepmind]
confidence: 0.90
created_at: 2026-05-11
sources:
  - https://github.com/google-deepmind/deepmind-research/tree/master/enformer
  - https://www.nature.com/articles/s41592-021-01252-x
---

# Enformer

Enformer is a deep learning architecture based on the [[transformer|Transformer]] that predicts gene expression from DNA sequences with base-pair resolution, surpassing previous convolution-based approaches.

## Architecture

Enformer combines:

- **Convolutional Stem**: Initial local feature extraction from raw DNA sequences
- **Transformer Blocks**: Global attention mechanisms to capture long-range regulatory interactions
- **Multiple Heads**: Predicts diverse molecular phenotypes simultaneously (gene expression, chromatin accessibility, transcription factor binding)

## Key Innovation

The use of [[attention_mechanism|attention]] allows Enformer to model regulatory interactions across distances of 100kb+ in the genome, far beyond the receptive field of convolutional models. The architecture is inspired by [[vision_transformer|Vision Transformers (ViT)]] adapted to 1D sequence data.

## Technical Details

| Aspect | Specification |
|--------|--------------|
| Input | DNA sequence (one-hot encoded, ~200kb context) |
| Architecture | Conv stem + 8 Transformer blocks |
| Output | 5,313 genomic tracks (expression, accessibility, etc.) |
| Resolution | Base-pair level predictions |

## Biological Insights

Enformer has been used to:
- Predict the impact of genetic variants on gene expression
- Identify regulatory elements and [[enhancer|enhancers]]
- Understand [[gene_regulation|gene regulation]] mechanisms

## Connection to Embodied Intelligence

While Enformer operates in the genomic domain, its architectural principles — particularly the use of attention for very long-range dependency modeling — have implications for temporal reasoning in embodied agents that must integrate information over extended time horizons.

## See Also

- [[deepmind_alphafold|AlphaFold]] — DeepMind's protein structure predictor
- [[transformer|Transformer Architecture]]
- [[attention_mechanism|Attention Mechanism]]
