---
id: tumf_mcp_text_editor
type: entity
title: tumf/mcp-text-editor
tags:
- mcp-server
- developer-tools
- text-editor
- llm-tools
- file-editing
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/tumf/mcp-text-editor
section: Server Implementations > 💻 <a name="developer-tools"></a>Developer Tools
---

> 🐍 🏠 - A line-oriented text file editor. Optimized for LLM tools with efficient partial file access to minimize token usage.

This project provides a Model Context Protocol (MCP) server for line-oriented text file editing, designed specifically for use with LLM tools. It offers efficient partial file access to minimize token usage, making it suitable for AI agents that need to read and modify files. The server supports operations like reading, writing, and editing text files line by line. It aims to reduce the overhead of full file reads by allowing targeted access to specific lines or ranges. This approach helps control costs and improves performance when working with large files through LLM interfaces.

**Category:** Server Implementations > 💻 <a name="developer-tools"></a>Developer Tools
**Source:** [https://github.com/tumf/mcp-text-editor](https://github.com/tumf/mcp-text-editor)
