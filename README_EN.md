<div align="center">

# 🤖 Awesome Agent Eval

**The Definitive Guide, Methodology & Engineering Toolkit for AI Agent Evaluation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](./README_EN.md) | [简体中文](./README.md) | [📚 Docs](./docs/) | [💻 Evals Code](./evals/) | [📊 Datasets](./datasets/)

</div>

---

## 📖 Introduction

As Large Language Models evolve from simple single-turn chatbots into autonomous **AI Agents** equipped with multi-step planning, tool calling, multi-turn interaction, and multi-agent coordination, traditional software assertions and basic Q&A evaluation metrics fall short.

**Awesome Agent Eval** provides an **industry-grade, end-to-end evaluation framework across the entire Agent lifecycle (Model Selection ➔ Component Testing ➔ Trajectory Evaluation ➔ Release Gates ➔ Production Observability)**, deeply integrating premier global benchmarks (**SWE-bench, OSWorld, Terminal-Bench, Meituan LongCat, TAU-bench, GAIA, BFCL**) and production-grade testing frameworks (**DeepEval, Ragas, Promptfoo, Inspect AI**).

---

## 🧭 Evaluation Landscape

```mermaid
graph TD
    A["Evaluation-Driven Development (EDD)"] --> B["1. Model Selection<br/>• Reverse-engineering capability profiles<br/>• Hard constraints & TCO tiering<br/>• Private dataset double-blind testing"]
    A --> C["2. Component Evaluation<br/>• Prompt variants & robustness<br/>• RAG 2-stage (Retrieval vs Generation)<br/>• Tool Calling 4-check & negative cases<br/>• Planning 3-failure-mode attribution"]
    A --> D["3. System Integration<br/>• Final outcomes (Pass@k vs Pass^k)<br/>• Trajectory matching (5 strictness tiers)<br/>• Dynamic User Simulator + Hidden Goal Cards<br/>• Multi-agent coordination & ablation"]
    A --> E["4. Release & Operations<br/>• 5 release quality gates (Quality/Cost/Security)<br/>• Production A/B testing (real traffic)<br/>• Observability (Logs/Traces/Metrics)<br/>• Bad-case regression flywheel"]
```

---

## 🛠️ Global Agent Evaluation Ecosystem Radar

| Domain | Benchmark / Framework | Institution / Repo | Core Evaluation Scope & Highlights |
| :--- | :--- | :--- | :--- |
| **Real Environments & Systems** | **SWE-bench** | [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench) (Princeton/OpenAI) | Real GitHub issue resolution verified by Docker unit test flips (FAIL $\rightarrow$ PASS) |
| | **OSWorld** | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) (HKU/Princeton) | Real Ubuntu OS multi-modal GUI + CLI cross-app (Office/Chrome/Terminal) evaluation |
| | **Terminal-Bench** | [princeton-nlp/intercode](https://github.com/princeton-nlp/intercode) (Princeton/Berkeley) | Linux Bash terminal sysadmin, troubleshooting & self-correction on execution feedback |
| | **VitaBench** | [meituan-longcat](https://github.com/meituan-longcat) (Meituan) | 3D POMDP life services complexity modeling, 66 tools, $\text{Pass}^4$ stress testing |
| | **TAU-bench** | [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) (Stanford/Sierra) | Dynamic customer service benchmark with sandbox DB transaction rollback checks |
| | **GAIA** | [gaia-benchmark](https://huggingface.co/spaces/gaia-benchmark/leaderboard) (Meta/HF) | Multi-modal, multi-step complex general assistant long-horizon tasks (Reverse Turing Test) |
| | **BFCL** | [Gorilla-LLM/BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) (UC Berkeley) | Authoritative tool calling & parallel function calling leaderboard |
| **Testing Frameworks** | **DeepEval** | [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | Production-ready Agent unit testing, G-Eval custom rubrics, CI/CD integration |
| | **Ragas** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | Standard for RAG retrieval quality, faithfulness & multi-agent communication |
| | **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | Blazing-fast CLI for prompt iteration and automated red-teaming security scans |
| | **Inspect AI** | [UK-AI-Safety-Institute/inspect_ai](https://github.com/UK-AI-Safety-Institute/inspect_ai) | UK AISI framework for enterprise/government safety & long-horizon capability eval |
| | **DSPy** | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | Stanford framework for metric-driven programmatic prompt compilation & auto-tuning |
| **Observability & Tracing**| **AgentOps** | [AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops) | Multi-agent execution graph tracing, loop detection, and token cost breakdown |
| | **Phoenix** | [Arize-AI/phoenix](https://github.com/Arize-AI/phoenix) | Open-source LLM/RAG observability & UMAP semantic drift clustering |

---

## 🐱 Spotlight: Meituan LongCat Research Series

We provide in-depth analysis and tracking of the Meituan LongCat team's frontier research:

| Project / Paper | Category | Core Contribution & Eval Significance | Links |
| :--- | :---: | :--- | :--- |
| **VitaBench** | Benchmark | 3D POMDP task complexity modeling, 66-tool dependency graph, and $\text{Pass}^4$ stress testing | [Deep Dive](./docs/07-case-studies.md) |
| **LongCat-Next** | Paper | *Lexicalizing Modalities as Discrete Tokens*: Native unified multimodal discrete autoregression | [Paper (arXiv:2603.27538)](https://arxiv.org/pdf/2603.27538) · [GitHub](https://github.com/meituan-longcat/LongCat-Next) |
| **LongCat-Flash** | Tech Report | Ultra-low latency online inference architecture, MoE routing, and long-context KV compression | [Paper (arXiv:2509.01322)](https://arxiv.org/abs/2509.01322) |

---

## 📚 Table of Contents

- [**01. 5 Core Dilemmas & EDD**](./docs/01-dilemmas-and-edd.md): Solving non-determinism, invisible processes, benchmark contamination, and judge biases.
- [**02. Universal Weapons**](./docs/02-general-weapons.md): Code metrics, Comparative evaluation (Position-Swap), and LLM-as-a-Judge rubrics.
- [**03. Model Selection & TCO**](./docs/03-model-selection.md): Capability profiling and hierarchical model routing.
- [**04. Component Evaluation**](./docs/04-component-eval.md): RAG precision/recall/faithfulness, tool hallucination defense, planning reflection errors.
- [**05. System Integration**](./docs/05-system-integration.md): 5-tier trajectory matching, dynamic multi-turn user simulation, and multi-agent ablation studies.
- [**06. Release Gates & Observability**](./docs/06-release-and-ops.md): 5 release gates, canary deployments, and data flywheel.
- [**07. Industry Case Studies**](./docs/07-case-studies.md): SWE-bench, OSWorld, Terminal-Bench, Meituan LongCat Series, TAU-bench, and GAIA.
- [**08. 23 Interview Flashcards**](./docs/08-interview-cards.md): High-frequency interview Q&A.
- [**09. Global Ecosystem Radar**](./docs/09-awesome-tools-and-frameworks.md): 18 top toolkits & platform selection matrix.

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Anlon-27/awesome-agent-eval.git
cd awesome-agent-eval
pip install -r requirements.txt
```

### 2. Run Ready-to-use Evals
```bash
# 1. Tool calling & negative hallucination test
python evals/tool_eval_demo.py

# 2. RAG two-stage precision & faithfulness test
python evals/rag_eval_demo.py

# 3. Dynamic User Simulator with goal shifts
python evals/user_simulator_demo.py

# 4. Position-Swap debiased LLM judge
python evals/swap_judge_demo.py
```

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
