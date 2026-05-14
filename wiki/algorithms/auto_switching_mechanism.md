---
id: auto_switching_mechanism
title: Auto-Switching Mechanism
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:39:14'
last_reinforced: '2026-04-29T21:39:14'
supersedes: []
sources:
- papers/2509.08699.pdf
source_type: arxiv_paper
---

## Auto-Switching Mechanism

The **Auto-Switching Mechanism** is an algorithmic component of the TANGO framework that enables automatic fallback to a baseline controller when TANGO's local control module outputs are deemed unreliable. This mechanism ensures robustness and safety in real-time manipulation tasks by preventing unstable or erroneous actions from being executed on the hardware.

### Parameters

| Parameter | Value |
|-----------|-------|
| `fallback` | `baseline controller` — the control policy that is activated upon failure detection |

### Capabilities

- Automatically switches to a baseline controller when TANGO's local control is unreliable, thereby maintaining safe operation.

### Relationships

- **part_of**: TANGO — the Auto-Switching Mechanism is a built-in safety layer within the TANGO system.

### Context

The mechanism is triggered by uncertainty or failure signals from TANGO's local control loop. By invoking a pre-defined baseline controller (e.g., a classical PID or impedance controller), the system avoids executing potentially dangerous learned policies, thus bridging the gap between learned behaviors and deployment safety. This design is critical for sim-to-real transfer, where model confidence may degrade under novel conditions.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Auto-Switching Mechanism` --extends ⚠️--> `TANGO`
