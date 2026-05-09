---
id: large_scale_indoor_lsi_environments
title: Large-Scale Indoor (LSI) environments
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:34:51'
last_reinforced: '2026-04-29T20:34:51'
supersedes: []
sources:
- papers/2603.16166.json
source_type: arxiv_paper
---

# Large-Scale Indoor (LSI) Environments

**Large-Scale Indoor (LSI) environments** are complex, expansive indoor spaces such as hospitals and airport terminals. These environments are characterized by their vast scale, hierarchical layout, and the **sparse placement of signage**, which often leads to a **dynamic sense of direction** for navigators — even when conventional map-based wayfinding is available.

## Key Characteristics

- **Scale**: Spanning entire buildings or multi-wing complexes with numerous rooms, corridors, and zones.
- **Signage sparsity**: Signage is strategically placed but often insufficient for seamless navigation without prior knowledge or active cues.
- **Dynamic orientation**: The overall sense of direction can shift as a person moves through long corridors or between wings, making **semantic signage** — signs that carry contextual meaning (e.g., "Oncology Wing" or "Gate B12") — essential for efficient path planning.

## Capabilities

- **Navigation with semantic signage**: LSI environments support wayfinding by relying on semantic signs that convey functional or categorical information rather than purely geometric or metric coordinates.
- **Applicable to complex public facilities**: These environments are typical of hospitals, airport terminals, convention centers, and large transportation hubs.

## Relationships

- **used_in**: [[SignNav]] — The SignNav system is designed to operate specifically within LSI environments, leveraging their semantic signage to provide instruction-based navigation.

## See Also

- [[Sign Navigation]] ⚠️ (related approach)
- [[Semantic Localization]] ⚠️
- [[Large-Scale Indoor Mapping]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Large-Scale Indoor (LSI) environments` --[[related_to]] ⚠️--> `SignNav`
