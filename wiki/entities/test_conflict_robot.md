---
id: test_conflict_robot
title: Test Conflict Robot
type: entity
confidence: 0.8
sources:
- papers/test.pdf
tags: []
supersedes: []
---

# Test Robot

A test robot for validation.

## Parameters

- **Weight**: 35kg
- **Height**: 1.2m

### 待核实冲突

CONFLICT_START
field: weight
old_value: 35kg | old_source: existing
new_value: 38kg | new_source: papers/test.pdf
CONFLICT_END

CONFLICT_START
field: height
old_value: 1.2m | old_source: existing
new_value: 1.25m | new_source: papers/test2.pdf
CONFLICT_END

## See Also
- [[Robotics]] ⚠️

### 已裁决冲突
_These conflicts were adjudicated by the conflict resolution engine._
**Resolved:**
- **height** → `1.25m` (confidence: 1.00)
  - Reasoning: Resolved by tolerance merge: values ['1.2m', '1.25m'] are equivalent (relative_diff < 5%, relative_diff=0.04).
**Still unresolved:**
- **weight** — status: `unresolved`, pending_human_review
  - Best candidate: `38kg` (0.68)
  - Runner-up: `35kg` (0.50)
