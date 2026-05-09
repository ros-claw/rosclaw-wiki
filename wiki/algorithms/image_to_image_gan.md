---
id: image_to_image_gan
title: Image-to-Image GAN
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:59:22'
last_reinforced: '2026-04-30T01:59:22'
supersedes: []
sources:
- papers/2210.03112.pdf
source_type: arxiv_paper
---

### Image-to-Image GAN

**Image-to-Image GAN** is a class of generative adversarial networks designed to learn a mapping from an input image to an output image. In the context of embodied AI and vision-and-language navigation, it is employed to synthesize image observations from novel viewpoints, thereby increasing the diversity of training data.

#### Capabilities

- **Synthesize image observations from novel viewpoints** – The GAN generates photorealistic views that are not present in the original dataset, enabling agents to learn from a wider range of perspectives.

#### Usage

- **Used for [[data augmentation]] ⚠️ in [[VLN]] ⚠️** – By generating synthetic views, the model augments training datasets for vision-and-language navigation tasks, improving the robustness and generalization of navigation policies.

#### Relationship Notes

- `Image-to-Image GAN` implements the general [[GAN]] ⚠️ architecture.
- It depends on paired input-output image data for training (e.g., a source view and a target view from a different camera pose).
- The output of this algorithm is used as input to downstream navigation models, such as [[VLN-BERT]] or [[decision transformers]] ⚠️.

#### Source

- Based on arXiv paper 2210.03112, which investigates viewpoint synthesis for data augmentation in VLN.