---
id: exploration_policy
title: Exploration Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:46:58'
last_reinforced: '2026-04-30T02:46:58'
supersedes: []
sources:
- papers/2007.08037.pdf
source_type: arxiv_paper
---

# Exploration Policy

The **exploration policy** is a learned decision-making component within the Active Visual Information Gathering (AVIG) framework. Its primary function is to enable embodied agents to actively reduce uncertainty — both from ambiguous language instructions and incomplete perceptual observations — by strategically controlling *where*, *when*, and *how* to explore an environment.

## Capabilities

As a learned policy, it coordinates three distinct but interdependent behaviors:

- **Decides when and where to explore**: Rather than following a fixed path, the policy outputs moment-to-moment exploration commands based on the current state of uncertainty, directing the agent toward information-rich regions.
- **Decides what information to gather during exploration**: The policy selects which sensory modalities or viewpoints to prioritize — for example, approaching an object from multiple angles or zooming in on a specific visual feature that resolves ambiguity in the task instruction.
- **Adapts navigation decisions after exploration**: Information collected during an exploration phase is fed back into the policy, allowing subsequent navigation plans to be revised in light of newly resolved uncertainties.

## Role in AVIG

The exploration policy is a core algorithmic component *part of* the broader Active Visual Information Gathering (AVIG) architecture. In AVIG, an agent must actively choose what to look at next in order to disambiguate underspecified goals or partially observable environments. The exploration policy implements this "active" loop:

1. Observe the current environment and instruction.
2. Estimate remaining uncertainty (via an internal confidence or entropy measure).
3. Execute an exploration action that maximally reduces that uncertainty.
4. Integrate the newly gathered information into a revised plan.

## Related Concepts

- Active Visual Information Gathering (AVIG) — the framework this policy belongs to (`part_of` relationship)
- Uncertainty Estimation ⚠️ — the underlying signal the policy uses to drive exploration decisions
- Navigation Policy ⚠️ — often coupled with the exploration policy; the navigation policy executes movement while the exploration policy decides the *goal* of that movement
- Embodied Instruction Following ⚠️ — the task domain in which exploration policies are typically evaluated

## References

- Arxiv paper: *Active Visual Information Gathering for Embodied Instruction Following* (2007.08037)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Exploration Policy` --extends ⚠️--> `Active Visual Information Gathering (AVIG)`
