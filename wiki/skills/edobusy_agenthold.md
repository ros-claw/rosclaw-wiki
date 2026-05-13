---
id: edobusy_agenthold
type: concept
title: edobusy/agenthold
tags:
- mcp
- state-store
- concurrency-control
- sqlite
- agent-coordination
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/edobusy/agenthold
section: Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
---

> [![agenthold MCP server](https://glama.ai/mcp/servers/edobusy/agenthold/badges/score.svg)](https://glama.ai/mcp/servers/edobusy/agenthold) 🐍 🏠 🍎 🪟 🐧 - Shared versioned state store with optimistic concurrency control for coordinating concurrent AI agents. SQLite-backed claim/release locks and append-only audit log.

Agenthold is a shared, versioned state store designed to coordinate multiple AI agents operating concurrently. It uses optimistic concurrency control to manage conflicts and ensures data consistency. The system is backed by SQLite for claim/release locks and an append-only audit log, providing reliability and traceability.

**Category:** Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
**Source:** [https://github.com/edobusy/agenthold](https://github.com/edobusy/agenthold)
