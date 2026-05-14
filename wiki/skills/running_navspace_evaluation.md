---
id: running_navspace_evaluation
title: Running NavSpace Evaluation
type: skill
tags: []
confidence: 0.95
created_at: '2026-04-30T04:48:19'
last_reinforced: '2026-04-30T04:48:19'
supersedes: []
sources:
- code/TidalHarley_NavSpace/README.md
source_type: official_manual
---

# Running NavSpace Evaluation

This skill describes the procedure to execute evaluation pipelines for the NavSpace benchmark using the official codebase. NavSpace evaluation tests embodied agents (LLM-based, SNav, StreamVLN) on tasks like environment state estimation, spatial memory, and navigation planning within Habitat-Sim scenes from HM3D.

## Dependencies

- `habitat-sim` (with Python bindings)
- `habitat-lab ⚠️`
- HM3D assets (v0.2)
- Python packages from `requirements-*.txt` files

## Steps

1. Clone the NavSpace repository.
2. Install dependencies (see requirements).
3. Run `smoke_test.py` to verify the environment.
4. Validate the dataset (checks HM3D paths and scene configurations).
5. Run evaluation with the following command-line arguments:
   - `--profile` (e.g., `gemini-pro`, `snap`, `streamvln`)
   - `--task` (e.g., `environment_state`, `spatial_memory`, `navigation`)
   - `--hm3d-base-path` (path to HM3D assets)

## Capabilities

- Evaluate **LLM agents** (profile `gemini-pro`, etc.) using API keys.
- Evaluate **SNav agent** (profile `snap`).
- Evaluate **StreamVLN agent**.
- Merge shard results from parallel evaluations.
- Dry-run verification via `smoke_test.py`.

## Relationships

- **uses**: NavSpace datasets ⚠️, Habitat-Sim, LLM ⚠️ ⚠️ API keys, evaluation scripts (e.g., `run_llm_eval.py`, `merge_shard_results.py`).
- **depends_on**: Habitat-Sim, HM3D (specifically v0.2).

## Quick Start

```bash
python evaluation/run_llm_eval.py \
  --profile gemini-pro \
  --task environment_state \
  --hm3d-base-path /path/to/hm3d_v0.2
```

## Notes

- LLM ⚠️ ⚠️ agents require API keys to be set in environment variables.
- SNav and StreamVLN agents may need separate model weights.
- The merge script can combine shards generated from multiple processes: `python merge_shard_results.py --experiment-dir ./results`.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Running NavSpace Evaluation` --uses ⚠️ ⚠️--> `SNav`
- `Running NavSpace Evaluation` --uses ⚠️ ⚠️--> `StreamVLN`
