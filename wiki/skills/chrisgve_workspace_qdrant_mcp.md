---
id: chrisgve_workspace_qdrant_mcp
type: concept
title: ChrisGVE/workspace-qdrant-mcp
tags:
- qdrant
- tree-sitter
- semantic-chunking
- hybrid-search
- mcp-server
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/ChrisGVE/workspace-qdrant-mcp
section: Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
---

> [![workspace-qdrant-mcp MCP server](https://glama.ai/mcp/servers/ChrisGVE/workspace-qdrant-mcp/badges/score.svg)](https://glama.ai/mcp/servers/ChrisGVE/workspace-qdrant-mcp) 🦀 📇 🏠 🍎 🪟 🐧 - Project-scoped semantic workspace memory for AI coding assistants. Watches your project files, auto-indexes code and docs into Qdrant with tree-sitter semantic chunking, LSP integration, and hybrid search (dense + sparse + RRF). 6 MCP tools: store, search, retrieve, grep, list, rules.

This MCP server creates a semantic memory layer for AI coding assistants that is scoped to a specific project workspace. It automatically watches project files and indexes both code and documentation using tree-sitter for semantic chunking, storing embeddings in Qdrant. It integrates with LSP for context and supports hybrid search combining dense and sparse vectors with Reciprocal Rank Fusion. Six MCP tools are provided: store, search, retrieve, grep, list, and rules. The goal is to give AI assistants persistent, context-aware memory of the project's codebase to improve their assistance.

**Category:** Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
**Source:** [https://github.com/ChrisGVE/workspace-qdrant-mcp](https://github.com/ChrisGVE/workspace-qdrant-mcp)
