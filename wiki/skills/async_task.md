---
id: async_task
type: concept
title: async-task
tags:
- async
- background-jobs
- long-running-tasks
- timeout-handling
- task-queue
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://clawskills.sh/skills/enderfga-async-task
section: Table of Contents
---

> Execute long-running tasks without HTTP timeouts.

Async-task is a tool designed to handle long-running tasks that exceed typical HTTP request timeout limits. It allows users to initiate a task and receive a response immediately, with the task executing in the background. The task's progress or result can be retrieved later via polling or callback mechanisms. This approach avoids HTTP timeouts and improves user experience for time-intensive operations.

**Category:** Table of Contents
**Source:** [https://clawskills.sh/skills/enderfga-async-task](https://clawskills.sh/skills/enderfga-async-task)
