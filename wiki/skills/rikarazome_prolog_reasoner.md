---
id: rikarazome_prolog_reasoner
type: concept
title: rikarazome/prolog-reasoner
tags:
- prolog-reasoner
- mcp-server
- code-execution
- logic-programming
- swi-prolog
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/rikarazome/prolog-reasoner
section: Server Implementations > 👨‍💻 <a name="code-execution"></a>Code Execution
---

> [![rikarazome/prolog-reasoner MCP server](https://glama.ai/mcp/servers/rikarazome/prolog-reasoner/badges/score.svg)](https://glama.ai/mcp/servers/rikarazome/prolog-reasoner) 🐍 🏠 🍎 🪟 🐧 - SWI-Prolog execution for LLMs with CLP(FD), negation-as-failure, and recursion. Benchmarked 90% vs 73% LLM-only accuracy on 30 logic problems.

This is an MCP server that allows Large Language Models to execute SWI-Prolog programs, supporting constraint logic programming over finite domains (CLP(FD)), negation-as-failure, and recursion. It acts as a reasoning engine that offloads logic inference from the LLM to a dedicated Prolog interpreter. Benchmarked on 30 logic problems, it achieved 90% accuracy compared to 73% for LLM-only approaches. The server is cross-platform, written in Python, and integrates with the Model Context Protocol (MCP) to provide code execution capabilities.

**Category:** Server Implementations > 👨‍💻 <a name="code-execution"></a>Code Execution
**Source:** [https://github.com/rikarazome/prolog-reasoner](https://github.com/rikarazome/prolog-reasoner)
