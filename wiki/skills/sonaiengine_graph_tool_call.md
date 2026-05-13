---
id: sonaiengine_graph_tool_call
type: entity
title: SonAIengine/graph-tool-call
tags:
- tool-graph
- llm-context
- hybrid-search
- mcp-proxy
- openapi-specs
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/SonAIengine/graph-tool-call
section: Frameworks
---

> [![graph-tool-call MCP server](https://glama.ai/mcp/servers/SonAIengine/graph-tool-call/badges/score.svg)](https://glama.ai/mcp/servers/SonAIengine/graph-tool-call) 🐍 🏠 - When tool count exceeds LLM context limits, accuracy collapses (248 tools → 12%). graph-tool-call builds a tool graph from OpenAPI/MCP specs and retrieves multi-step workflows via hybrid search (BM25 + graph traversal + embedding), recovering accuracy to 82% with 79% fewer tokens. Zero dependencies. Also works as an MCP Proxy — aggregate multiple MCP servers behind 3 meta-tools.

graph-tool-call addresses the problem of LLM context limits when handling many tools, such as accuracy dropping to 12% with 248 tools. It builds a tool graph from OpenAPI/MCP specifications and retrieves multi-step workflows using hybrid search combining BM25, graph traversal, and embeddings, restoring accuracy to 82% while using 79% fewer tokens. This zero-dependency framework can also function as an MCP Proxy, aggregating multiple MCP servers behind three meta-tools. It aims to improve LLM tool-calling reliability and efficiency in tool-rich environments.

**Category:** Frameworks
**Source:** [https://github.com/SonAIengine/graph-tool-call](https://github.com/SonAIengine/graph-tool-call)
