---
id: low_level_planner
title: Low-Level Planner
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:36:33'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2601.04699.pdf
source_type: arxiv_paper
---

## Low-Level Planner

The **Low-Level Planner** is an algorithmic component within the [[SeqWalker]] system responsible for trajectory execution and error correction. It operates at the fine-grained action level, converting high-level sub-instructions into executable steps while continuously verifying progress.

### Role
The planner’s primary role is **trajectory execution and error correction**. It takes sub-instructions and real-time visual observations, then plans and refines robot motions to achieve the instructed goals.

### Strategy
The Low-Level Planner employs an **Exploration-Verification** strategy, which consists of two alternating phases:

- **Exploration**: The robot attempts to advance along the trajectory predicted by the high-level planner ([[High-Level Planner]]), executing actions based on the current sub-instruction.
- **Verification**: After each exploration step, the planner checks whether the action has been successfully completed or if a deviation occurred. If an error is detected (e.g., the robot is stuck or off-course), the exploration-verification loop triggers corrective motion.

This approach leverages the **inherent logical structure of instructions** to identify when a step has failed and to guide re-planning, allowing the system to recover autonomously from execution errors.

### Inputs
- Sub-instructions (from the [[High-Level Planner]] or intermediate goal descriptions)
- Visual observations (camera images, depth data, etc.) to assess progress

### Capabilities
- **Leverage instruction structure for error correction**: By understanding the sequential and logical relationships between sub-instructions, the planner can pinpoint which step went wrong and adjust the trajectory accordingly.
- **Exploration and verification of trajectory steps**: Systematically tests and validates each sub-goal before proceeding, ensuring robustness against dynamic environments.

These capabilities form the core of the planner’s design and have been confirmed by recent analyses of the SeqWalker framework.

### Relationships
- **part_of** [[SeqWalker]] – The Low-Level Planner is a core module of the SeqWalker architecture, which decomposes long-horizon tasks into hierarchical planning and execution.
- **uses** [[Exploration-Verification strategy]] – The core algorithmic pattern that governs how the planner handles trajectory steps and recovery.
- **uses** [[Instruction Structure]] ⚠️ – The logical ordering and dependencies embedded in the instruction language are exploited to inform verification and correction decisions.

### See Also
- [[High-Level Planner]] – Provides sub-instruction sequences to the Low-Level Planner.
- [[SeqWalker]] – The overall framework that integrates high- and low-level planners.
- [[Exploration-Verification strategy]] – Detailed description of the strategy used.