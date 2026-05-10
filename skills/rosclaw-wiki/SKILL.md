---
name: rosclaw-steward
description: >
  The ROSClaw Wiki knowledge steward for embodied intelligence.
  Manages a causal nexus of robot kinematics, material limits,
  algorithmic constraints, and real-world physics. Converts
  GitHub Awesome Lists and repositories into structured wikis,
  and serves them via FastAPI with physical constraint checking.
author: ROSClaw.io
version: 1.1.0
license: MIT
homepage: https://rosclaw.io
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "🗿"
    os: ["darwin", "linux", "win32"]
    requires:
      env: ["ROSClaw_API_KEY"]
      config: ["rosclaw-steward"]
    primaryEnv: "ROSClaw_API_KEY"
---

# ROSClaw Steward — Skill Directory

This repository is the **ROSClaw Wiki** knowledge engine. It is maintained
by three Claude Code skills located in `.claude/skills/`.

## Skill Map

| Skill | What It Does | When to Invoke |
|-------|-------------|----------------|
| **rosclaw-wiki-ingest** | Convert Awesome Lists / GitHub repos into wiki pages | "Ingest this awesome list" / "Add this repo to the wiki" |
| **rosclaw-wiki-dev** | Local setup, run API/MCP, debug, deploy | "How do I run this locally?" / "Why is the DB read-only?" |
| **rosclaw-wiki-api** | Endpoint reference, auth flow, frontend integration | "What endpoints are available?" / "How does auth work?" |

## Quick Reference by Task

### Task: Ingest a New Awesome List

```bash
# Step 1: Download raw sources
python rosclaw_fetch.py --input awesome-robotics.md --output-dir data/raw

# Step 2: Start MCP server
python mcp_wiki_server.py

# Step 3: Use MCP tools to extract entities and create pages
#   wiki_ingest_source → wiki_create_page → wiki_auto_lint

# Step 4: Verify in Obsidian (open wiki/ as vault)
```

Full guide: `.claude/skills/rosclaw-wiki-ingest/SKILL.md`

---

### Task: Set Up Local Development

```bash
# Python 3.11+
pip install -r requirements.txt
pip install -e .

# Run API
python -m uvicorn commercial_api:app --reload

# Run MCP server (stdio)
python mcp_wiki_server.py
```

Full guide: `.claude/skills/rosclaw-wiki-dev/SKILL.md`

---

### Task: Call the API from a Frontend

```typescript
// After NextAuth.js OAuth login:
const res = await fetch("https://api.rosclaw.io/wiki/v1/auth/exchange", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: user.email, name: user.name }),
});
const { api_key } = await res.json();
localStorage.setItem("rosclaw_api_key", api_key);

// All subsequent requests:
fetch("https://api.rosclaw.io/wiki/v1/auth/me", {
  headers: { "X-API-Key": localStorage.getItem("rosclaw_api_key") },
});
```

Full guide: `.claude/skills/rosclaw-wiki-api/SKILL.md`

---

## Core Philosophy: "Connection is Intelligence"

Wisdom arises not from knowing a fact, but from understanding the
**relationships** between facts.

- A single node is meaningless.
- Two nodes connected form a **constraint**.
- A thousand nodes interwoven form a **physical theory**.

When an agent queries `max_torque = 237 N·m`, you do not just return
the number. You return the **subgraph**: the gear ratio that defines it,
the thermal ceiling that limits it, the paper that measured it,
and the URDF that enforced it. This is **Physical Context**.

## Three Phases of Grounding

### Phase 1 — Cognitive Grounding ("Where am I?")
- **Tools**: `search_wiki`, `get_judgments`
- **Goal**: Understand the entity's place in the topology

### Phase 2 — Relational Tracing ("What if?")
- **Tools**: `topology_trace`, `sensitivity_analysis`
- **Goal**: Map every affected node and edge

### Phase 3 — Truth Anchoring ("Is this real?")
- **Tools**: `physics_feasibility`, `reasoning_grounding`
- **Goal**: Anchor LLM-generated intent against physical reality

## Installation (for End Users)

```bash
# 1. Clone
git clone https://github.com/ros-claw/rosclaw-wiki.git
cd rosclaw-wiki

# 2. Install
pip install -r requirements.txt
pip install -e .

# 3. Get API key (via OAuth or manual)
export ROSClaw_API_KEY="rw_sk_your_key_here"

# 4. Verify
curl -H "X-API-Key: $ROSClaw_API_KEY" https://api.rosclaw.io/v1/health
```

## API Documentation

https://api.rosclaw.io (interactive docs at `/docs` when running locally)

For complete endpoint reference: `.claude/skills/rosclaw-wiki-api/SKILL.md`
