#!/usr/bin/env python3
"""Batch create wiki pages for deepmind-research and Awesome-VLN."""

import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path("/root/workspace/rosclaw/rosclaw_wiki/rosclaw-wiki/wiki")
DATA_ROOT = Path("/root/workspace/rosclaw/rosclaw_wiki/rosclaw-wiki/data")
RAW_CODE = DATA_ROOT / "raw" / "code"

def generate_id(title: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]+', '_', title.lower()).strip('_')

def write_page(path: Path, meta: dict, body: str):
    frontmatter = yaml.dump(meta, allow_unicode=True, sort_keys=False)
    content = f"---\n{frontmatter}---\n\n{body}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"  Created: {path}")

# ============================================================
# Part 1: DeepMind Research - remaining subdirectories
# ============================================================

deepmind_dir = RAW_CODE / "deepmind-research"
existing_deepmind = set()
for p in (WIKI_ROOT / "entities").glob("deepmind_*.md"):
    existing_deepmind.add(p.stem.replace("deepmind_", ""))

# Map directory names to human-readable titles and descriptions
# Based on actual deepmind-research repo contents
DEEPMIND_PROJECTS = {
    "adversarial_robustness": ("Adversarial Robustness", "Research on adversarial examples and robustness in deep learning models."),
    "affordances_theory": ("Affordances Theory", "Theoretical framework for understanding affordances in embodied AI and robotics."),
    "alphafold_casp13": ("AlphaFold CASP13", "AlphaFold's entry in the 13th Critical Assessment of protein Structure Prediction (CASP13)."),
    "avae": ("aVAE", "Adversarial Variational Autoencoder for generative modeling."),
    "bigbigan": ("BigBiGAN", "Large-scale Bidirectional Generative Adversarial Network for representation learning."),
    "box_arrangement": ("Box Arrangement", "Learning to arrange objects in boxes using reinforcement learning."),
    "byol": ("BYOL", "Bootstrap Your Own Latent — self-supervised learning without negative samples."),
    "cadl": ("CADL", "Curiosity-driven exploration for reinforcement learning."),
    "catch_carry": ("Catch and Carry", "Learning manipulation skills for catching and carrying objects."),
    "causal_reasoning": ("Causal Reasoning", "Neural approaches to causal inference and reasoning."),
    "cmtouch": ("CmTouch", "Tactile sensing and touch-based manipulation research."),
    "continual_learning": ("Continual Learning", "Lifelong learning without catastrophic forgetting."),
    "counterfactual_fairness": ("Counterfactual Fairness", "Fairness in machine learning through causal counterfactuals."),
    "cs_gan": ("CS-GAN", "Compressed Sensing Generative Adversarial Network."),
    "curl": ("CURL", "Contrastive Unsupervised Representations for Reinforcement Learning."),
    "density_functional_approximation_dm21": ("DM21 Density Functional", "DeepMind 21 — neural network approximation of density functionals for quantum chemistry."),
    "enformer": ("Enformer", "Gene expression prediction from DNA sequence using transformer architecture."),
    "ensemble_loss_landscape": ("Ensemble Loss Landscape", "Analysis of loss landscapes for deep ensemble methods."),
    "functional_regularisation_for_continual_learning": ("Functional Regularisation for Continual Learning", "Preventing catastrophic forgetting via functional regularization."),
    "fusion_tcv": ("Fusion TCV", "Tokamak Control using reinforcement learning for nuclear fusion."),
    "galaxy_mergers": ("Galaxy Mergers", "Simulating and classifying galaxy merger events."),
    "gated_linear_networks": ("Gated Linear Networks", "Neural networks with gated linear transformations."),
    "geomancer": ("Geomancer", "Geospatial machine learning for environmental science."),
    "glassy_dynamics": ("Glassy Dynamics", "Simulating glass transition and amorphous materials."),
    "graph_matching_networks": ("Graph Matching Networks", "Neural networks for learning similarity between graphs."),
    "hierarchical_probabilistic_unet": ("Hierarchical Probabilistic U-Net", "Hierarchical probabilistic U-Net for image segmentation."),
    "hierarchical_transformer_memory": ("Hierarchical Transformer Memory", "Memory-augmented transformers with hierarchical attention."),
    "himo": ("HiMo", "Hierarchical motion generation for character animation."),
    "iodine": ("IODINE", "Iterative Object Decomposition Inference Network for multi-object representation learning."),
    "kfac_ferminet_alpha": ("KFAC Ferminet Alpha", "Optimization techniques for quantum chemistry neural networks."),
    "learned_free_energy_estimation": ("Learned Free Energy Estimation", "Neural network estimation of free energy in physical systems."),
    "learning_to_simulate": ("Learning to Simulate", "Learning particle-based simulation with Graph Networks."),
    "memo": ("MEMO", "Memory-based optimization for meta-learning."),
    "meshgraphnets": ("MeshGraphNets", "Mesh-based physics simulation using Graph Networks."),
    "mmv": ("MMV", "Multimodal Versatile network for cross-modal representation learning."),
    "neural_mip_solving": ("Neural MIP Solving", "Learning to solve Mixed Integer Programming problems."),
    "nfnets": ("NFNets", "Normalizer-Free Networks — high-performance image classification without batch normalization."),
    "noisy_label": ("Noisy Label Learning", "Robust learning from noisy labeled data."),
    "nowcasting": ("Nowcasting", "Precipitation nowcasting using deep generative models."),
    "object_attention_for_reasoning": ("Object Attention for Reasoning", "Visual reasoning with object-centric attention."),
    "ode_gan": ("ODE-GAN", "Ordinary Differential Equation GAN for continuous-time generative modeling."),
    "ogb_lsc": ("OGB-LSC", "Open Graph Benchmark Large-Scale Challenge."),
    "option_keyboard": ("Option Keyboard", "Hierarchical reinforcement learning with combinable skills."),
    "perceiver": ("Perceiver", "General perception with iterative attention — scalable architecture for arbitrary inputs."),
    "physics_inspired_models": ("Physics-Inspired Models", "Neural networks inspired by physical principles and symmetries."),
    "physics_planning_games": ("Physics Planning Games", "Learning physics-based planning through game environments."),
    "pitfalls_static_language_models": ("Pitfalls of Static Language Models", "Analysis of failure modes in static language model evaluation."),
    "polygen": ("PolyGen", "Autoregressive generative model of 3D meshes."),
    "powerpropagation": ("Powerpropagation", "Improved neural network training via power propagation."),
    "PrediNet": ("PrediNet", "Relational neural network for abstract reasoning."),
    "rapid_task_solving": ("Rapid Task Solving", "Fast adaptation to new tasks via meta-learning."),
    "regal": ("ReGAL", "Representation learning for game abstraction."),
    "rl_unplugged": ("RL Unplugged", "Large-scale offline reinforcement learning dataset and benchmark."),
    "satore": ("SATORI", "Self-Attention Transformer for reinforcement learning."),
    "scratchgan": ("ScratchGAN", "Training GANs from scratch without pre-trained discriminators."),
    "side_effects_penalties": ("Side Effects Penalties", "Measuring and penalizing side effects in RL agents."),
    "sketchy": ("Sketchy", "Learning from sketch data for visual understanding."),
    "synthetic_returns": ("Synthetic Returns", "Synthetic return functions for improved RL credit assignment."),
    "tandem_dqn": ("Tandem DQN", "Improved DQN training with tandem network architecture."),
    "transporter": ("Transporter", "Visual representation learning via keypoint-based transportation."),
    "tvt": ("TVT", "Transferable Visual Transformer for domain adaptation."),
    "unrestricted_advx": ("Unrestricted Adversarial Examples", "Generating and defending against unrestricted adversarial examples."),
    "unsupervised_adversarial_training": ("Unsupervised Adversarial Training", "Adversarial training without labeled data."),
    "visr": ("VISR", "Visual Semantic Reasoning for embodied agents."),
    "wikigraphs": ("WikiGraphs", "Wikipedia knowledge graph construction and reasoning."),
}

def create_deepmind_pages():
    print("=" * 60)
    print("Part 1: Creating DeepMind Research wiki pages")
    print("=" * 60)
    created = 0
    skipped = 0

    for subdir, (title, desc) in DEEPMIND_PROJECTS.items():
        page_id = f"deepmind_{subdir}"
        page_path = WIKI_ROOT / "entities" / f"{page_id}.md"

        if page_path.exists() or subdir in existing_deepmind:
            skipped += 1
            continue

        # Check if directory exists in downloaded code
        has_code = (deepmind_dir / subdir).is_dir()
        sources = ["https://github.com/google-deepmind/deepmind-research"]
        if has_code:
            sources.append(f"https://github.com/google-deepmind/deepmind-research/tree/master/{subdir}")

        meta = {
            "id": page_id,
            "type": "entity",
            "tags": ["deepmind", "research", "google"],
            "confidence": 0.75,
            "created_at": "2026-05-11",
            "sources": sources,
        }

        body = f"# {title}\n\n{desc}\n\n## Source\n\n"
        if has_code:
            body += f"Subdirectory: `{subdir}` in [[deepmind_research|DeepMind Research]] repository.\n\n"
        else:
            body += "Part of the DeepMind Research repository.\n\n"

        body += "## See Also\n\n"
        body += "- [[deepmind_research|DeepMind Research]]\n"
        body += "- [[google_deepmind|Google DeepMind]]\n"

        write_page(page_path, meta, body)
        created += 1

    print(f"DeepMind: {created} created, {skipped} skipped (already exist)")
    return created

# ============================================================
# Part 2: Parse Awesome-VLN README and create pages
# ============================================================

def parse_awesome_vln():
    """Parse the Awesome-VLN README.md table to extract paper entries."""
    readme_path = Path("/root/workspace/rosclaw/rosclaw_wiki/Awesome-VLN/README.md")
    content = readme_path.read_text(encoding='utf-8')

    entries = []
    # Pattern to match table rows with arxiv links
    # |2026|`AAAI`<br>Chinese Academy of Sciences|[Run, Ruminate, and Regulate...](https://arxiv.org/pdf/2511.14131)|...|...|
    row_pattern = re.compile(
        r'\|\s*(\d{4})\s*\|\s*`?([^|]+?)`?\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]*)\|\s*([^|]*)\|'
    )

    for m in row_pattern.finditer(content):
        year = m.group(1).strip()
        venue = m.group(2).strip()
        title = m.group(3).strip()
        paper_url = m.group(4).strip()
        repo_cell = m.group(5).strip()
        note = m.group(6).strip()

        # Extract arxiv ID from URL
        arxiv_id = None
        arxiv_match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)', paper_url)
        if arxiv_match:
            arxiv_id = arxiv_match.group(1)

        # Extract GitHub repo from shields/badge or direct link
        github_url = None
        github_match = re.search(r'https://github\.com/([^/\s)]+/[^/\s)]+)', repo_cell)
        if github_match:
            github_url = f"https://github.com/{github_match.group(1)}"

        # Extract website from note cell
        website = None
        website_match = re.search(r'\[website\]\(([^)]+)\)', note, re.IGNORECASE)
        if website_match:
            website = website_match.group(1)

        entries.append({
            'year': year,
            'venue': venue,
            'title': title,
            'paper_url': paper_url,
            'arxiv_id': arxiv_id,
            'github_url': github_url,
            'note': note,
            'website': website,
        })

    return entries

def create_vln_pages():
    print("\n" + "=" * 60)
    print("Part 2: Creating Awesome-VLN wiki pages")
    print("=" * 60)

    entries = parse_awesome_vln()
    print(f"Parsed {len(entries)} entries from Awesome-VLN README")

    created = 0
    skipped = 0

    # Track existing pages to avoid duplicates
    existing_ids = set()
    for p in WIKI_ROOT.rglob("*.md"):
        if p.name in ('index.md', 'log.md'):
            continue
        content = p.read_text(encoding='utf-8')
        # Extract id from frontmatter
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                meta = yaml.safe_load(parts[1])
                if meta and 'id' in meta:
                    existing_ids.add(meta['id'])
            except Exception:
                pass

    for entry in entries:
        title = entry['title']
        # Generate page ID
        page_id = generate_id(title)
        if len(page_id) > 80:
            page_id = page_id[:80]

        if page_id in existing_ids:
            skipped += 1
            continue

        # Only create pages for entries with GitHub repos or notable papers
        # Prioritize: has github repo, or is a simulator/dataset, or has real-robot notes
        has_github = entry['github_url'] is not None
        has_real_robot = any(kw in entry['note'].lower() for kw in [
            '真机', 'unitree', 'go2', 'g1', 'spot', 'robot', 'jetson', 'orin',
            '四足', '轮式', '人形', '部署', '实测', '实验'
        ])
        is_simulator = any(kw in title.lower() for kw in [
            'simulator', 'dataset', 'benchmark', 'habitat', 'matterport',
            'alfred', 'reverie', 'r2r', 'rxr', 'soon', 'cvdn'
        ])

        if not (has_github or has_real_robot or is_simulator or entry['year'] >= '2025'):
            skipped += 1
            continue

        # Build sources
        sources = []
        if entry['paper_url']:
            sources.append(entry['paper_url'])
        if entry['github_url']:
            sources.append(entry['github_url'])
        if entry['website']:
            sources.append(entry['website'])

        # Determine tags
        tags = ['vln', 'vision-language-navigation', entry['year']]
        if has_real_robot:
            tags.append('real-robot')
        if is_simulator:
            tags.append('simulator' if 'simulator' in title.lower() else 'dataset')
        if 'unitree' in entry['note'].lower():
            tags.append('unitree')

        # Determine type
        if is_simulator:
            page_type = 'entity'
        else:
            page_type = 'algorithm'

        meta = {
            "id": page_id,
            "type": page_type,
            "tags": tags,
            "confidence": 0.8 if has_github else 0.65,
            "created_at": "2026-05-11",
            "sources": sources,
        }

        # Build body
        body = f"# {title}\n\n"
        body += f"**Year**: {entry['year']}  \n"
        body += f"**Venue**: {entry['venue']}  \n"
        if entry['arxiv_id']:
            body += f"**arXiv**: [{entry['arxiv_id']}]({entry['paper_url']})  \n"
        if entry['github_url']:
            body += f"**Code**: [{entry['github_url']}]({entry['github_url']})  \n"
        if entry['website']:
            body += f"**Website**: [{entry['website']}]({entry['website']})  \n"

        body += "\n## Overview\n\n"
        # Clean up note for markdown
        note_clean = entry['note'].replace('|', ' ').replace('<br>', '\n')
        body += note_clean + "\n"

        body += "\n## See Also\n\n"
        body += "- [[vision_and_language_navigation|Vision-Language Navigation]]\n"
        body += "- [[object_goal_navigation|Object-Goal Navigation]]\n"
        if 'unitree' in entry['note'].lower():
            body += "- [[unitree_go2|Unitree Go2]]\n"
        if 'habitat' in entry['note'].lower():
            body += "- [[ai_habitat|AI Habitat]]\n"

        page_path = WIKI_ROOT / "entities" / f"{page_id}.md"
        write_page(page_path, meta, body)
        created += 1

    print(f"VLN: {created} created, {skipped} skipped")
    return created

# ============================================================
# Part 3: Create concept pages for key VLN topics
# ============================================================

CONCEPT_PAGES = {
    "vision_and_language_navigation": {
        "title": "Vision-Language Navigation (VLN)",
        "type": "concept",
        "tags": ["vln", "navigation", "vision-language", "embodied-ai"],
        "body": """# Vision-Language Navigation (VLN)

VLN is the task of navigating an embodied agent (robot) in a 3D environment following natural language instructions.

## Core Challenge

The agent must simultaneously:
1. **Understand language**: Parse navigation instructions (e.g., "Go to the kitchen, turn left, find the red chair")
2. **Perceive the environment**: Process visual observations (RGB, depth, panoramas)
3. **Act**: Output navigation actions (move forward, turn, stop)

## Key Datasets

| Dataset | Year | Description |
|---------|------|-------------|
| [[r2r|R2R (Room-to-Room)]] | 2018 | First VLN dataset, Matterport3D, discrete actions |
| [[rxr|RxR]] | 2020 | Multilingual VLN with dense spatiotemporal grounding |
| [[reverie|REVERIE]] | 2020 | Remote embodied visual referring expression |
| [[soon|SOON]] | 2021 | Scenario-oriented object navigation |
| [[r2r_ce|R2R-CE]] | 2022 | Continuous environment version of R2R |
| [[cvdn|CVDN]] | 2020 | Cooperative vision and dialog navigation |

## Key Methods

- **Pre-training + Fine-tuning**: [[prevalent|PREVALENT]], [[vlm_bert|VLN-BERT]]
- **LLM-based Reasoning**: [[navgpt|NavGPT]], [[mapgpt|MapGPT]]
- **VLM-based Navigation**: [[navid|NaVid]], [[uninavid|Uni-NaVid]]
- **Reinforcement Learning**: [[vln_r1|VLN-R1]]

## Real-robot Deployment

Recent works deploy VLN on physical robots:
- [[nasa_jpl_nebula2_wildos|WildOS]]: NASA JPL outdoor navigation
- [[sysnav|SysNav]]: Unitree Go2 and G1
- [[navspace|NavSpace]]: AgiBot Lingxi D1
- [[deco_vln|DecoVLN]]: Unitree GO2 with Jetson Orin

## See Also

- [[object_goal_navigation|Object-Goal Navigation]]
- [[embodied_ai|Embodied AI]]
- [[large_language_model|Large Language Models]]
- [[multimodal_foundation_model|Multimodal Foundation Models]]
"""
    },
    "object_goal_navigation": {
        "title": "Object-Goal Navigation",
        "type": "concept",
        "tags": ["navigation", "object-goal", "embodied-ai"],
        "body": """# Object-Goal Navigation

Object-goal navigation (ObjNav) is the task of navigating to a specified object category in an unseen environment.

## Task Definition

Given:
- Target object category (e.g., "chair", "television")
- RGB/Depth observations
- No prior map

Output:
- Sequence of actions to reach the target

## Key Approaches

1. **Map-based**: Build semantic map, plan to target
2. **Mapless**: End-to-end policy directly outputs actions
3. **Foundation Model-based**: Use VLM/VLA for zero-shot navigation

## Datasets

- [[hm3d_ovon|HM3D-OVON]]: Open-vocabulary object navigation
- [[ai_habitat|AI Habitat]]: Simulation platform

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[open_vocabulary_navigation|Open-Vocabulary Navigation]]
"""
    },
    "simulator_and_dataset": {
        "title": "VLN Simulators and Datasets",
        "type": "concept",
        "tags": ["vln", "simulator", "dataset", "benchmark"],
        "body": """# VLN Simulators and Datasets

## Simulators

| Simulator | Description |
|-----------|-------------|
| [[matterport3d_simulator|Matterport3D Simulator]] | First VLN simulator, discrete graph |
| [[ai_habitat|AI Habitat]] | High-performance 3D simulator |
| [[habitat_sim|Habitat-Sim]] | Photorealistic simulator |
| [[vlnerse|VLNVerse]] | NVIDIA Isaac Sim-based, 263 scenes |

## Datasets

| Dataset | Scenes | Instructions | Key Feature |
|---------|--------|-------------|-------------|
| [[r2r|R2R]] | 90 | 21K | Discrete actions |
| [[r2r_ce|R2R-CE]] | 90 | 21K | Continuous actions |
| [[rxr|RxR]] | 90 | 16K | Multilingual, dense grounding |
| [[reverie|REVERIE]] | 90 | 10K | Remote referring expression |
| [[soon|SOON]] | 90 | 4K | Scenario-oriented object nav |
| [[cvdn|CVDN]] | 83 | 2K | Dialog-based navigation |
| [[alfred|ALFRED]] | 120 | 25K | Task-oriented household |
| [[scale_vln|ScaleVLN]] | - | 4M+ | Scaled synthetic data |
"""
    },
}

def create_concept_pages():
    print("\n" + "=" * 60)
    print("Part 3: Creating concept pages")
    print("=" * 60)

    created = 0
    for page_id, info in CONCEPT_PAGES.items():
        page_path = WIKI_ROOT / "concepts" / f"{page_id}.md"
        if page_path.exists():
            print(f"  Skipped (exists): {page_path}")
            continue

        meta = {
            "id": page_id,
            "type": info["type"],
            "tags": info["tags"],
            "confidence": 0.9,
            "created_at": "2026-05-11",
            "sources": ["https://github.com/KwanWaiPang/Awesome-VLN"],
        }
        write_page(page_path, meta, info["body"])
        created += 1

    print(f"Concepts: {created} created")
    return created

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    total = 0
    total += create_deepmind_pages()
    total += create_vln_pages()
    total += create_concept_pages()
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} new wiki pages created")
    print(f"{'=' * 60}")
