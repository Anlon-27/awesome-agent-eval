<div align="center">

# 🤖 Awesome Agent Eval

**The Definitive Methodology, Architecture & Engineering Toolkit for AI Agent Evaluation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](./README_EN.md) | [简体中文](./README.md) | [📚 Whitepaper](./docs/01-framework-and-edd.md) | [🚀 Adoption SOP](./docs/02-enterprise-adoption-sop.md) | [💻 Evaluation Code](./evals/) | [📊 Benchmark Datasets](./datasets/)

</div>

---

## 📖 Mission & 4D Orthogonal Architecture

As LLMs transition into autonomous **AI Agents** capable of planning, tool use, long-term memory, environmental interactions, and multi-agent collaboration, traditional software assertions (`assert response == expected`) and simple QA scores fail catastrophically.

**Awesome Agent Eval** establishes the industry-standard **4D Orthogonal Evaluation Matrix** and **Evaluation-Driven Development (EDD)** paradigm:
* **Dimension 1: Target Layers (What: L0 ~ L4)**: Foundation Models ➔ Atomic Components ➔ Planning & State Machines ➔ End-to-End Sandboxes ➔ Multi-Agent Systems;
* **Dimension 2: Metrics Pyramid (How: 4-Tier Metrics)**: Deterministic Assertions ➔ Trajectory Quality ➔ Business Value ROI ➔ Engineering NFRs;
* **Dimension 3: Execution & Arbiters (Engine: 4 Levels)**: Code Assertions ➔ Docker/ACI Sandboxes ➔ Adversarial Simulators ➔ Position-Swap LLM Judges;
* **Dimension 4: MLOps Lifecycle & Data Flywheel (Lifecycle: Dev to Flywheel)**: Micro-evals ➔ 5 Release Gates ➔ Production Shadow Runs ➔ Badcase Self-Evolving Flywheels.

```mermaid
flowchart TD
    classDef stageBox fill:#f8fafc,stroke:#3b82f6,stroke-width:2px,rx:8px,ry:8px;
    classDef stepNode fill:#ffffff,stroke:#cbd5e1,stroke-width:1.5px,color:#0f172a;

    subgraph D1["📘 Dimension 1: Target Layers (L0 ~ L4)"]
        direction TB
        L0["L0: Foundation LLM (IFEval / Reasoning / TCO Routing)"]
        L1["L1: Atomic Components (Prompts / 2-Stage RAG / Tool Schemas)"]
        L2["L2: Planning & State (ReAct / DAG Workflows / POMDP / Reflection)"]
        L3["L3: End-to-End Tasks (Docker Sandboxes / DB State Diff / User Simulators)"]
        L4["L4: Multi-Agent Systems (Protocol / Role Drift / Consensus / Ablation)"]
        L0 --> L1 --> L2 --> L3 --> L4
    end

    subgraph D2["📊 Dimension 2: Metrics Pyramid"]
        direction TB
        M1["Business Value Tier (Task Success Rate / Pass^k / Human Intervention)"]
        M2["Trajectory Quality Tier (Effective Step Ratio / Tool Accuracy / Drift)"]
        M3["Atomic Precision Tier (Exact Match / JSON Schema 100% / State Diff)"]
        M4["Engineering NFR Tier (P99 Latency / Token Budget / Fallback Rate)"]
        M1 --- M2 --- M3 --- M4
    end

    subgraph D3["⚙️ Dimension 3: Engines & Arbiters"]
        direction TB
        E1["Level 1: Deterministic Code Assertions (Regex / Pydantic / Exit Codes)"]
        E2["Level 2: Isolated Sandboxes (Docker / Linux ACI / DB Rollback)"]
        E3["Level 3: Adversarial Simulators (Dynamic User Simulators with Hidden Goals)"]
        E4["Level 4: LLM-as-a-Judge (Rubrics / Position-Swap Bias Elimination)"]
        E1 --> E2 --> E3 --> E4
    end

    subgraph D4["🔄 Dimension 4: Lifecycle & Flywheel"]
        direction TB
        P1["Phase 1 (Dev): Micro-evals & Prompt A/B Exploration"]
        P2["Phase 2 (CI/CD): 5 Release Gates & Blocking Pipelines"]
        P3["Phase 3 (Prod): Shadow Runs & Online A/B Experimentation"]
        P4["Phase 4 (Flywheel): Badcase Auto-Clustering -> Sanitization -> Testset Enrichment"]
        P1 --> P2 --> P3 --> P4 --> P1
    end

    D1 -. "Maps to" .-> D2
    D3 -. "Drives" .-> D4
    D1 ==> D3
    D2 ==> D4

    %% Safe bottom padding: Prevents GitHub floating zoom controller from occluding diagram nodes
    subgraph SafePadding[" "]
        direction LR
        padNode["&nbsp;<br>&nbsp;<br>&nbsp;"]
    end
    style SafePadding fill:transparent,stroke:transparent;
    style padNode fill:transparent,stroke:transparent,color:transparent;
    D3 ~~~ SafePadding
    D4 ~~~ SafePadding

    class D1,D2,D3,D4 stageBox;
    class L0,L1,L2,L3,L4,M1,M2,M3,M4,E1,E2,E3,E4,P1,P2,P3,P4 stepNode;
```

---

## 📚 12-Chapter Comprehensive Whitepaper Syllabus

| Chapter & Link | Framework Dimension | Core Insights & Practice Guide |
| :--- | :--- | :--- |
| [**01. Framework & EDD**](./docs/01-framework-and-edd.md) | **Foundational Meta-Model** | 4D Orthogonal Architecture, Metrics Pyramid, 5 Dilemmas, and EDD Methodology |
| [**02. Enterprise Adoption SOP**](./docs/02-enterprise-adoption-sop.md) | **Engineering SOP** | Day 1~7 (Cold Start) ➔ Day 8~30 (CI/CD Gates) ➔ Day 31~60 (Simulation) ➔ Day 61~90 (Production Flywheel) |
| [**03. L0 Foundation Model Eval**](./docs/03-l0-foundation-model-eval.md) | **Target Layer L0** | 4-step Selection, IFEval Instruction Following, Needle in a Haystack, and Flagship/SLM Routing TCO |
| [**04. L1 Atomic Components Eval**](./docs/04-l1-atomic-components-eval.md) | **Target Layer L1** | Prompt Micro-Evals, 2-Stage RAG (NDCG/Faithfulness), Tool Calling 5-point Checklist & Anti-Hallucination |
| [**05. L2 Planning & State Eval**](./docs/05-l2-planning-and-state-eval.md) | **Target Layer L2** | ReAct Stability, DAG Workflow Transitions, POMDP State Modeling, Loop Breakers, and Reflection |
| [**06. L3 End-to-End System Eval**](./docs/06-l3-end-to-end-system-eval.md) | **Target Layer L3** | 5-Tier Trajectory Rubric, Docker Physical State Diff (DB/FS), Dynamic User Simulators, Pass^k Robustness |
| [**07. L4 Multi-Agent Systems Eval**](./docs/07-l4-multi-agent-eval.md) | **Target Layer L4** | Protocol Overhead, Role Drift Auditing, Consensus Rounds, Deadlock Detection, and Topology Ablations |
| [**08. Metrics & Judge Arsenal**](./docs/08-metrics-and-judge-arsenal.md) | **Metrics & Arbiters** | Deterministic Code Assertions, NLP/Semantic Metrics (BERTScore), G-Eval Rubrics & Position-Swap Debias |
| [**09. Engineering NFR Eval**](./docs/09-engineering-nfr-eval.md) | **Cross-Cutting NFR** | Perturbation Robustness (Punctuation/Typos), JSON Schema 100% Compliance, API 500 Fallback & Latency |
| [**10. Benchmark Schemas & Datasets**](./docs/10-benchmark-schemas-and-cases.md) | **Global Benchmarks** | In-depth breakdown & JSON Schemas for SWE-bench, OSWorld, Terminal-Bench, and VitaBench |
| [**11. Autonomous Coding & GUI Agents**](./docs/11-autonomous-coding-and-gui.md) | **Vertical Frontiers** | OpenHands (CodeAct EventStream) & SWE-Agent (ACI Interface) Deep Architecture & Sandbox Verification |
| [**12. Release Gates, Platforms & Flywheel**](./docs/12-platform-gates-and-flywheel.md) | **Production & MLOps** | 5 Release Gates, 5-Layer Platform Architecture, Production Data Flywheel, and 25 Engineering FAQs |

---

## ⚡ Quick Start: Running Automated Evals

```bash
# 1. Tool calling precision and anti-hallucination test
python evals/tool_eval_demo.py

# 2. Two-stage RAG evaluation (Retrieval Context Precision & Generation Faithfulness)
python evals/rag_eval_demo.py

# 3. Dynamic multi-turn adversarial User Simulator test
python evals/user_simulator_demo.py

# 4. Position-Swap double-blind LLM judge test (First-position bias elimination)
python evals/swap_judge_demo.py

# 5. Robustness against prompt perturbations, JSON schema validation, and API 500 fallback
python evals/robustness_and_fallback_demo.py
```

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
