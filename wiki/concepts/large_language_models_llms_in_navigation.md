---
id: large_language_models_llms_in_navigation
title: Large Language Models (LLMs) in Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:20:07'
last_reinforced: '2026-04-30T01:20:07'
supersedes: []
sources:
- papers/2407.12366.pdf
source_type: arxiv_paper
---

## Overview

Large Language Models (LLMs) represent a transformative paradigm in embodied navigation, serving as the central reasoning engine that bridges natural language understanding with physical action selection. In the context of robot navigation, LLMs are employed to parse complex, diverse language instructions and generalize navigational reasoning across unseen environments. This approach departs from traditional mapping+planning pipelines by leveraging the broad world knowledge and instruction-following capabilities inherent in pretrained language models.

## Capabilities

LLMs in navigation demonstrate two key capabilities:

- **Generalize navigational reasoning**: Instead of requiring task-specific training for every possible instruction variation, LLMs can interpret commands like "go to the blue door" or "avoid the obstacle on the left" using commonsense and contextual understanding. This generalization is critical for deployment in unstructured human environments.
- **Understand diverse language instructions**: From spatially grounded commands ("move 2 meters forward") to goal-oriented requests ("find the kitchen"), LLMs can parse a wide range of linguistic forms, including synonyms, ambiguous references, and multi-step instructions.

## Integration

LLMs are integrated with navigation policy networks to produce both actions and accompanying reasoning chains. In typical architectures, the LLM receives textual observations (e.g., a description of the scene or a list of detected objects) and outputs action tokens (e.g., "turn left", "move forward") which are then mapped to low-level motor commands by a separate policy network. This dual-output design allows the system to explain its decisions in natural language while simultaneously executing commands.

Notable implementations include NavGPT-2, which uses an LLM-powered tokenization of visual and language inputs to generate navigational reasoning and action sequences. The LLM also serves as the backbone for reasoning about subgoals (e.g., "first go to the corridor, then the living room") and handling replanning when obstacles are encountered.

## Relationships

- **Used in**: NavGPT-2, LLM-based navigation paradigms ⚠️
- **Implements**: *navigational reasoning* (concept), *language instruction following* (concept)
- **Depends on**: Navigation policy networks ⚠️ for low-level control, pretrained language models ⚠️ as backbone
- **Contradicts**: traditional rule-based or ML-only navigators that cannot handle open-ended language
- **Labels**: concept, reasoning, navigation, language understanding, embodied AI

## Key Observations

The integration of LLMs into navigation systems enables zero-shot generalization to new instructions and environments, at the cost of increased inference latency and computational overhead. The paper from which this page is derived (sources: papers/2407.12366 ⚠️) emphasizes that LLM-based navigators like NavGPT-2 can match or exceed state-of-the-art task completion rates on benchmarks such as R2R and REVERIE, while providing transparent reasoning logs.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Large Language Models (LLMs) in Navigation` --related_to ⚠️--> `NavGPT-2` _(wikilink)_
