---
id: run_claude_docker
type: entity
title: run-claude-docker
tags:
- docker-runner
- claude-code
- workspace-isolation
- credential-forwarding
- tooling
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/icanhasjonas/run-claude-docker
section: Tooling > General
---

> A self-contained Docker runner that forwards your current workspace into a safe(r) isolated docker container, where you still have access to your Claude Code settings, authentication, ssh agent, pgp, optionally aws keys etc.

This project provides a Docker runner that forwards your current workspace into an isolated Docker container while preserving access to Claude Code settings, authentication, SSH agent, PGP, and optional AWS keys. It aims to create a safer development environment by containing the workspace without losing critical tooling and credentials. The tool is designed for users who want to run Claude Code or similar AI agents with reduced risk of affecting the host system.

**Category:** Tooling > General
**Source:** [https://github.com/icanhasjonas/run-claude-docker](https://github.com/icanhasjonas/run-claude-docker)
