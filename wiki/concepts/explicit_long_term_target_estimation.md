---
id: explicit_long_term_target_estimation
title: Explicit long-term target estimation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:11:23'
last_reinforced: '2026-04-30T02:11:23'
supersedes: []
sources:
- papers/2207.11201.pdf
source_type: arxiv_paper
---

## Explicit Long-term Target Estimation

**Explicit long-term target estimation** is a [[concept]] ⚠️ in embodied AI that enables an agent to infer the ultimate navigation goal location even when that target is not yet visible from the current viewpoint. The agent leverages a combination of visual observations and linguistic instructions to predict where the target *should be*, rather than relying solely on reactive local planning.

### Description

The ability to explicitly predict the ultimate goal location, even when it is not yet visible, using a combination of visual and linguistic information. This contrasts with implicit methods that only learn a policy mapping from observations to actions without forming an explicit representation of the target's spatial location.

### Capabilities

- Allows inference of navigation targets in completely unexplored or occluded areas based on visual-linguistic clues.
- Enables the agent to plan toward a distant goal without needing to have seen it previously.

### Related Concepts

| Relationship | Linked Page | Notes |
|---|---|---|
| `related_to` | TD-STP ⚠️ | Explicit long-term target estimation is a core idea within the TD-STP (Temporal Distance and Spatial Temporal Planning) framework. |
| `implements` | Imaginary Scene Tokenization ⚠️ ⚠️ | Imaginary Scene Tokenization ⚠️ ⚠️ is a method that realizes explicit long-term target estimation by generating "imaginary" scene tokens representing the target location. |
| `depends_on` | Visual-Linguistic Grounding ⚠️ | The estimation requires aligning visual features with linguistic descriptions to infer the target. |
| `used_in` | Embodied Navigation | This concept is a key component in advanced goal-conditioned navigation systems. |

### References

- Source: `data/raw/papers/2207.11201.pdf` — details the use of explicit long-term target estimation in a navigation agent.