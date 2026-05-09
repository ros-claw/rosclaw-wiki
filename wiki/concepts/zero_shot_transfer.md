---
id: zero_shot_transfer
title: Zero-Shot Transfer
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:37:51'
last_reinforced: '2026-04-30T04:37:51'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# Zero-Shot Transfer

**Zero-Shot Transfer** is a [[Sim-to-Real Transfer]] paradigm in which two independently trained components (e.g., a navigation policy and a locomotion policy) are deployed together at test time without any joint fine-tuning or co-adaptation. This eliminates the need for expensive co-training loops or shared reward engineering across subsystems.

## Definition

The ability to deploy two separately trained components together without any joint training. In the context of the [[ViNL]] system, the navigation policy’s velocity commands are directly fed to the locomotion policy at test time — no additional gradient updates, adaptation layers, or bridging modules are introduced.

## Parameters

| Parameter | Value |
|-----------|-------|
| Domain    | Sim-to-Real |
| Modality  | Policy co-deployment without co-training |

- **Domain**: zero-shot transfer is primarily exercised in [[Sim-to-Real Transfer]] pipelines, where simulated training must generalise to real hardware without online retraining.
- **Modality**: policies are trained independently (navigation in one simulator, locomotion in another, possibly with different observation spaces) and only combined at inference time.

## Capabilities

- Combine independently trained navigation and locomotion policies without additional fine-tuning or co-adaptation.
- Reduce deployment complexity by avoiding joint training procedures that require synchronised environments or shared reward signals.
- Enable modular policy development: locomotion experts can be swapped or upgraded without retraining the navigation policy and vice versa.

## Relationships

- **Used by**: [[ViNL]] uses zero-shot transfer to bridge the output of its navigation policy (high-level velocity commands) with the low-level locomotion controller.
- **Related to**: [[Sim-to-Real Transfer]] — zero-shot transfer is a specific class of sim-to-real techniques that rely on robust policy representations rather than online adaptation.

## Example

In the ViNL architecture, a navigation policy trained via reinforcement learning in a static simulator outputs linear and angular velocity commands. These commands are directly fed to a locomotion policy trained in a separate physics environment (e.g., for a quadruped robot). Despite the two policies never being trained jointly, the system successfully traverses real-world paths, demonstrating zero-shot transfer.

## Limitations

Zero-shot transfer depends on the compatibility of action and observation spaces between the two components. If the navigation policy outputs velocities outside the locomotion policy’s stable range, the deployment fails without post-hoc scaling. Similarly, sim-to-real gaps in either component can compound and break the transfer.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-Shot Transfer` --[[related_to]] ⚠️--> `ViNL` _(wikilink)_
