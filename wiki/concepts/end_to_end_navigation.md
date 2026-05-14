---
id: end_to_end_navigation
title: End-to-end navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:26:14'
last_reinforced: '2026-04-30T03:26:14'
supersedes: []
sources:
- papers/2512.19629.pdf
source_type: arxiv_paper
---

# End-to-end Navigation

**End-to-end navigation** refers to a learning-based approach that maps raw sensor inputs directly to control commands or trajectories, bypassing the traditional perception-to-planning pipeline. Instead of decomposing navigation into separate modules for mapping, localization, path planning, and control, a single model (often a deep neural network) attempts to learn the entire mapping from sensor data to action.

## Capabilities

- **Reduces latency and cascading errors** — by removing intermediate processing stages and their error propagation.
- **Improves performance in open-world settings** — the learned model can adapt to complex, unstructured environments that are difficult to model explicitly.
- **Enables joint optimization of perception and planning** — the entire system can be trained end-to-end to maximize a navigation reward, rather than optimizing each module independently.

## Relationships

- **Contradicts** Traditional Modular Pipelines ⚠️ — the classical approach separates navigation into distinct components (sensing → mapping → localization → planning → control), which can suffer from error accumulation and hand-tuned interfaces.
- **Exemplified by** LoGoPlanner — a system that extends end-to-end design to include implicit localization, addressing a common weakness of pure end-to-end methods.

## Advantages

End-to-end methods promise greater efficiency and generalization, but many still rely on separate localization modules. LoGoPlanner extends end-to-end design to include implicit localization, demonstrating that even traditionally modular components can be absorbed into a learned framework.

While end-to-end navigation has shown promise in simulation and controlled trials, practical deployments often require careful handling of safety, sim-to-real transfer, and the ability to recover from out-of-distribution sensor inputs. The field continues to explore hybrid approaches that blend learned policies with traditional planners for robustness.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `End-to-end navigation` --related_to ⚠️--> `LoGoPlanner` _(wikilink)_
