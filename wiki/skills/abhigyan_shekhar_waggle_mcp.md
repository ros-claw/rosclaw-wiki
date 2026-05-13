---
id: abhigyan_shekhar_waggle_mcp
type: concept
title: Abhigyan-Shekhar/Waggle-mcp
tags:
- persistent-memory
- graph-memory
- mcp-server
- knowledge-graph
- semantic-embeddings
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/Abhigyan-Shekhar/Waggle-mcp
section: Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
---

> [![Abhigyan-Shekhar/Waggle-mcp MCP server](https://glama.ai/mcp/servers/Abhigyan-Shekhar/Waggle-mcp/badges/score.svg)](https://glama.ai/mcp/servers/Abhigyan-Shekhar/Waggle-mcp) 🐍 🏠 🍎 🪟 🐧 - Persistent graph memory for AI agents. Drop a conversation turn in via `observe_conversation()` and facts are auto-extracted, stored as typed graph nodes with local semantic embeddings (no API key). Supports temporal queries ("what did we decide last week?"), conflict detection, and context priming. One-command setup with `waggle-mcp init`. SQLite locally, Neo4j in production.

Waggle-mcp is an MCP server that gives AI agents persistent, graph-based memory. By calling a function called `observe_conversation()`, agents can store conversation turns as typed nodes in a graph, with facts automatically extracted and embedded locally—no external API key required. It supports time-aware queries like 'what did we decide last week?', detects conflicting facts, and primes context on recall. The system runs on SQLite for local use and Neo4j in production, and can be set up with a single command.

**Category:** Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
**Source:** [https://github.com/Abhigyan-Shekhar/Waggle-mcp](https://github.com/Abhigyan-Shekhar/Waggle-mcp)
