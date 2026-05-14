---
id: read_only_postgres
type: skill
title: read-only-postgres
tags:
- postgresql
- read-only
- database-query
- claude-code
- agent-skill
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/jawwadfirdousi/agent-skills
section: Agent Skills > General
---

> Read-only PostgreSQL query skill for Claude Code. Executes SELECT/SHOW/EXPLAIN/WITH queries across configured databases with strict validation, timeouts, and row limits. Supports multiple connections with descriptions for database selection.

This is a read-only PostgreSQL query skill designed for Claude Code, an AI agent framework. It allows executing safe queries like SELECT, SHOW, EXPLAIN, and WITH statements across multiple configured databases. The skill enforces strict validation, timeouts, and row limits to prevent accidental data modification or excessive resource usage. It supports multiple database connections with descriptive labels for easy selection within agent interactions.

**Category:** Agent Skills > General
**Source:** [https://github.com/jawwadfirdousi/agent-skills](https://github.com/jawwadfirdousi/agent-skills)
