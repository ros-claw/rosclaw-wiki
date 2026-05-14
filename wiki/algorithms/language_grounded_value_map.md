---
id: language_grounded_value_map
title: Language-grounded value map
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:32:27'
last_reinforced: '2026-04-30T04:32:27'
supersedes: []
sources:
- papers/2312.03275.pdf
source_type: arxiv_paper
---

# Language-Grounded Value Map

The **Language-grounded value map** is a key component of the VLFM (Vision-Language Frontier Maps) system. It assigns a semantic relevance score to each frontier in an exploration map, indicating how likely that frontier is to lead to a target object specified by a natural language category. By leveraging a pre-trained vision-language model, the map grounds spatial exploration in language, enabling robots to efficiently search for objects described by text.

## Inputs & Outputs

| Input | Description |
|-------|-------------|
| Frontier locations | Candidate exploration points in the environment |
| RGB images | Visual observations captured at each frontier |
| Target category text | A natural-language description of the object to find (e.g., "mug", "chair") |

| Output | Description |
|--------|-------------|
| Value scores | A scalar per frontier indicating its estimated relevance to the target object |

## Capabilities

- **Semantic scoring**: Uses a pre-trained vision-language model to compute a similarity score between the RGB observation at a frontier and the target category text.
- **Guides frontier selection**: The VLFM system uses these value scores to prioritize frontiers that are more likely to contain the target object, making exploration task-directed rather than purely information-theoretic.

## How It Works

1. For each frontier, an RGB image is captured (e.g., from the robot’s onboard camera).
2. The image and the target category text are fed into a pre-trained vision-language model (e.g., CLIP).
3. The model outputs a similarity score (or logit) representing how well the image matches the target concept.
4. This score is stored as the value for that frontier in a spatial map.
5. The VLFM system then selects frontiers with the highest value scores, balancing exploration with object search.

## Relationships

- **Part of**: VLFM — the language-grounded value map is a core module that implements the semantic grounding for frontier selection.
- **Uses**: Pre-trained vision-language model (e.g., CLIP) to compute cross-modal similarity.
- **Depends on**: Frontier exploration ⚠️ to supply candidate locations and corresponding RGB images.

## References

- Source: [arxiv 2312.03275](https://arxiv.org/abs/2312.03275) — *VLFM: Vision-Language Frontier Maps for Zero-Shot Object Goal Navigation*.

*(This page was created from structured facts extracted from the paper; see also VLFM for the overall system architecture.)*