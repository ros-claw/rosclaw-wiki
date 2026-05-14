---
id: tsk_ai_agent_task_manager_and_sandbox
type: entity
title: TSK - AI Agent Task Manager and Sandbox
tags:
- ai-agents
- cli
- docker-sandbox
- rust
- task-orchestration
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/dtormoen/tsk
section: Tooling > Orchestrators
---

> A Rust CLI tool that lets you delegate development tasks to AI agents running in sandboxed Docker environments. Multiple agents work in parallel, returning git branches for human review.

TSK is a command-line tool written in Rust that enables developers to delegate software development tasks to multiple AI agents. These agents work in isolated Docker containers to ensure safety, and they can operate in parallel to complete tasks efficiently. The final output from each agent is provided as a Git branch, which can be reviewed and merged by a human developer. TSK serves as an orchestrator that coordinates multiple AI agents for complex development workflows.

**Category:** Tooling > Orchestrators
**Source:** [https://github.com/dtormoen/tsk](https://github.com/dtormoen/tsk)
