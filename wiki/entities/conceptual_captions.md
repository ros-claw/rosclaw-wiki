---
id: conceptual_captions
title: Conceptual Captions
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T03:04:26'
last_reinforced: '2026-04-30T03:04:26'
supersedes: []
sources:
- papers/2004.14973.pdf
source_type: arxiv_paper
---

# Conceptual Captions

**Conceptual Captions** is a large-scale dataset of image-text pairs automatically collected from the web, used to pretrain visiolinguistic models. It provides abundant image-text pairs for pretraining, enabling models to learn visual grounding and multimodal representations.

## Description

Conceptual Captions is a large-scale dataset of image-text pairs automatically collected from the web, used to pretrain visiolinguistic models. The dataset consists of approximately 3.3 million images paired with descriptive captions curated through an automatic pipeline, filtering noisy web data to produce high-quality annotations. It is widely employed in vision-language pretraining due to its scale and diversity.

## Parameters

- **Type**: image-text dataset
- **Source**: web-scraped

## Capabilities

- Provide abundant image-text pairs for pretraining

## Relationships

- **Used by**: VLN-BERT — Conceptual Captions is used as a pretraining dataset for the VLN-BERT model.
- **Supports**: Visual Grounding — The dataset enables learning of visual grounding tasks by mapping language to image regions.

Conceptual Captions depends on Web Scraping ⚠️ for data collection and is related to other image-text datasets such as COCO Captions ⚠️ and Flickr30k ⚠️.