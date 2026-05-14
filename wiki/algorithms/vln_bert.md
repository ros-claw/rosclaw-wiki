---
id: vln_bert
title: VLN-BERT
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:09:06'
last_reinforced: '2026-04-30T02:09:06'
supersedes: []
sources:
- papers/2004.14973.pdf
source_type: arxiv_paper
---

VLN-BERT is a visiolinguistic transformer model designed for Vision-and-Language Navigation (VLN) ⚠️ ⚠️. It scores the compatibility between a natural language instruction and a sequence of panoramic RGB images, enabling an agent to evaluate candidate paths. The key innovation is pretraining on large-scale web-scraped image-text pairs before fine-tuning on embodied path-instruction data, which significantly improves VLN performance.

**Architecture**  
The model uses a Transformer architecture ⚠️ ⚠️ to jointly encode visual and linguistic inputs. It processes a sequence of panoramic RGB images (captured from different viewpoints along a trajectory) and a textual instruction. An output score indicates how well the instruction describes the visual sequence.

**Training Data & Strategy**  
- **Pretraining**: Conceptual Captions (web-scraped image-text pairs)  
- **Fine-tuning**: Embodied path-instruction data (e.g., from VLN datasets)  

## Pretraining Curriculum
The model was pretrained on image-text pairs from the web before fine-tuning on embodied path-instruction data, showing synergistic effects from combining stages. This two-stage curriculum bridges the gap between static visual grounding and dynamic navigation tasks.

**Capabilities**  
- Score compatibility between an instruction and a sequence of panoramic RGB images.  
- Improve VLN performance via pretraining on web data.

**Relationships**  
- *uses*: Conceptual Captions  
- *depends_on*: Transformer architecture ⚠️ ⚠️, Visual Grounding  
- *improves*: Vision-and-Language Navigation (VLN) ⚠️ ⚠️