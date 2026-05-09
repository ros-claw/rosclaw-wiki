# Full Text vs Abstract Knowledge Extraction Report

**Paper:** 2602.19308
**Date:** 2026-04-28
**Model:** deepseek (deepseek-v4-flash)

## Text Statistics

| Metric | Abstract Only | Full Text |
|--------|--------------|-----------|
| Characters | 1886 | 97657 (22896 focused section chars used for LLM) |
| Source | PDF extraction (abstract section) | PDF extraction (PyMuPDF) |

## Extraction Results

| Metric | Abstract | Full Text | Gain |
|--------|----------|-----------|------|
| Entities extracted | 8 | 20 | 2.5x |
| Parameters extracted | 9 | 40 | 4.4x |
| Capabilities extracted | 16 | 33 | 2.1x |
| Relationships extracted | 16 | 37 | 2.3x |

## Abstract Entities

```json
[
  {
    "entity_type": "algorithm",
    "entity_name": "WildOS",
    "new_facts": {
      "parameters": {
        "type": "unified system for long-range open-vocabulary object search"
      },
      "capabilities": [
        "safe geometric exploration",
        "semantic visual reasoning",
        "sparse navigation graph maintenance",
        "real-time onboard semantic navigation"
      ],
      "relationships": {
        "uses": [
          "ExploRFM",
          "Particle-filter localization for open-vocabulary objects",
          "Sparse navigation graph"
        ],
        "depends_on": [
          "Vision foundation models"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "algorithm",
    "entity_name": "ExploRFM",
    "new_facts": {
      "parameters": {
        "type": "foundation-model-based vision module",
        "function": "simultaneously predict traversability, visual frontiers, and object similarity in image space"
      },
      "capabilities": [
        "traversability prediction",
        "visual frontier scoring",
        "object similarity scoring"
      ],
      "relationships": {
        "used_by": [
          "WildOS"
        ],
        "depends_on": [
          "Vision foundation models"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "algorithm",
    "entity_name": "Particle-filter localization for open-vocabulary objects",
    "new_facts": {
      "parameters": {
        "method": "coarse localization of open-vocabulary target query",
        "function": "estimate candidate goal positions beyond robot's immediate depth horizon"
      },
      "capabilities": [
        "coarse localization beyond depth horizon",
        "planning toward distant goals"
      ],
      "relationships": {
        "used_by": [
          "WildOS"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "concept",
    "entity_name": "Sparse navigation graph",
    "new_facts": {
      "parameters": {
        "purpose": "maintain spatial memory"
      },
      "capabilities": [
        "enable real-time semantic navigation tasks"
      ],
      "relationships": {
        "part_of": [
          "WildOS"
        ],
        "used_by": [
          "ExploRFM"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "algorithm",
    "entity_name": "Geometric frontier exploration",
    "new_facts": {
      "parameters": {},
      "capabilities": [
        "exploration based on geometric frontiers",
        "insufficient in complex unstructured environments"
      ],
      "relationships": {
        "compared_with": [
          "WildOS"
        ],
        "used_in": [
          "baseline comparison"
        ]
      }
    },
    "source_type": "arxiv_paper"
  }
]
```

## Full Text Entities (first 5)

```json
[
  {
    "entity_type": "entity",
    "entity_name": "Boston Dynamics Spot",
    "new_facts": {
      "parameters": {
        "type": "quadruped robot platform"
      },
      "capabilities": [
        "outdoor locomotion",
        "onboard compute hosting"
      ],
      "relationships": {
        "uses": [
          "Ouster OS0-128 LiDAR",
          "VectorNav VN-100 IMU",
          "Intel RealSense D455",
          "Intel NUC i7",
          "NVIDIA Jetson AGX Orin"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "entity",
    "entity_name": "Ouster OS0-128 LiDAR",
    "new_facts": {
      "parameters": {
        "type": "LiDAR sensor",
        "channels": 128
      },
      "capabilities": [
        "3D point cloud acquisition"
      ],
      "relationships": {
        "used_by": [
          "Boston Dynamics Spot"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "entity",
    "entity_name": "VectorNav VN-100 IMU",
    "new_facts": {
      "parameters": {
        "type": "inertial measurement unit"
      },
      "capabilities": [
        "inertial sensing for localization"
      ],
      "relationships": {
        "used_by": [
          "Boston Dynamics Spot"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "entity",
    "entity_name": "Intel RealSense D455 RGB-D Camera",
    "new_facts": {
      "parameters": {
        "type": "RGB-D camera",
        "quantity": 3,
        "mounting": [
          "left",
          "front",
          "right"
        ]
      },
      "capabilities": [
        "RGB image capture",
        "depth sensing"
      ],
      "relationships": {
        "used_by": [
          "Boston Dynamics Spot"
        ]
      }
    },
    "source_type": "arxiv_paper"
  },
  {
    "entity_type": "entity",
    "entity_name": "Intel NUC i7",
    "new_facts": {
      "parameters": {
        "type": "onboard computer",
        "processor": "Intel Core i7"
      },
      "capabilities": [
        "running localization (DLIO)",
        "local motion planning (Nav2)"
      ],
      "relationships": {
        "used_by": [
          "Boston Dynamics Spot"
        ]
      }
    },
    "source_type": "arxiv_paper"
  }
]
```

## Conclusion

Full-text extraction provides **2.5x more entities** and **4.4x more parameters** than abstract-only extraction.
This validates that PDF full-text extraction is essential for deep knowledge extraction.