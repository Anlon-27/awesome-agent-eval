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

**Awesome Agent Eval** provides an **industry-grade, end-to-end evaluation curriculum and platform engineering framework**.

This project covers **core NLP/LLM metrics (Accuracy, BLEU, BERTScore, NDCG)**, mainstream frameworks (**OpenCompass, LM-Evaluation-Harness, DeepEval, Ragas**), **enterprise evaluation platform architecture designs, standard JSON schemas, and runnable automation test scripts**.

---

## 🧭 5-Stage Progressive Learning Roadmap

```mermaid
graph TD
    subgraph STAGE1["Stage 1: Foundations & Core Metrics"]
        D1["01. 5 Core Dilemmas & EDD"] --> D2["02. Core Metrics: Accuracy / BLEU / BERTScore / LLM Judge"]
    end

    subgraph STAGE2["Stage 2: Model Selection & Component Evals"]
        D2 --> D3["03. Model Selection, Capability Profiling & TCO Tiering"]
        D3 --> D4["04. 4 Component Evals (Prompt / RAG / Tools / Planning)"]
        D4 --> D5["05. 4 Core Engineering Dimensions (RAG / Perturbation / Schema / Fallbacks)"]
    end

    subgraph STAGE3["Stage 3: System Integration & Frontier Benchmarks"]
        D5 --> D6["06. System Integration (5-Tier Trajectory / User Simulator / Multi-Agent Ablation)"]
        D6 --> D7["07. Global Benchmark Schemas (SWE-bench / OSWorld / Terminal / VitaBench)"]
        D7 --> D8["08. Autonomous Coding Agents (OpenHands & SWE-Agent ACI Architectures)"]
    end

    subgraph STAGE4["Stage 4: Platforms, Release Gates & Ecosystem"]
        D8 --> D9["09. 5 Release Quality Gates, A/B Testing & Data Flywheel"]
        D9 --> D10["10. Evaluation Platforms (OpenCompass/LM-Eval) & Platform Architecture"]
    end

    subgraph STAGE5["Stage 5: Interview Mastery"]
        D10 --> D11["11. 23 Comprehensive Interview Flashcards & Standard Answers"]
    end
```

---

## 📊 NLP & LLM Core Evaluation Metrics Matrix

| Metric Name | Mathematical Principles | Target Scenarios | Official GitHub / Libraries |
| :--- | :--- | :--- | :--- |
| **Accuracy** | Proportion of correct predictions ($\frac{TP+TN}{Total}$) | Multiple choice (MMLU), Classification | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **Exact Match (EM)** | 100% exact match after normalization | Tool names, slot extraction, status codes | [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **BLEU (1~4)** | Modified n-gram precision + Brevity Penalty (BP) | Machine translation, code gen (HumanEval) | [`nltk`](https://github.com/nltk/nltk) / [`sacrebleu`](https://github.com/mjpost/sacrebleu) |
| **ROUGE (1/2/L)** | Longest Common Subsequence (LCS) recall-oriented | Text summarization, document synthesis | [`google-research/rouge`](https://github.com/google-research/google-research) |
| **BERTScore** | Contextual embedding maximum cosine similarity | Open Q&A, paraphrase similarity | [`Tiiiger/bert_score`](https://github.com/Tiiiger/bert_score) *(ICLR 2020)* |
| **NDCG@k / MRR** | Normalized Discounted Cumulative Gain & MRR | RAG retrieval ranking quality | [`ranx`](https://github.com/AmenDa/ranx) / [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) |

---

## 🛠️ Mainstream Evaluation Platforms & Frameworks Ecosystem Radar

| Domain | Platform / Benchmark | Institution / Repo | Core Evaluation Scope & Highlights |
| :--- | :--- | :--- | :--- |
| **Mainstream Platforms** | **OpenCompass** | [open-compass/opencompass](https://github.com/open-compass/opencompass) (Shanghai AI Lab) | **Leading one-stop full-stack evaluation platform**, multi-modal Hub & distributed task runner |
| | **LM-Evaluation-Harness** | [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | The de facto global standard powering Hugging Face Open LLM Leaderboard |
| | **DeepEval** | [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | Production-ready Agent unit testing, G-Eval custom rubrics, CI/CD integration |
| | **HELM** | [stanford-crfm/helm](https://github.com/stanford-crfm/helm) (Stanford University) | Holistic evaluation across accuracy, robustness, fairness, bias & toxicity |
| | **Ragas** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | Standard for RAG retrieval quality, faithfulness & multi-agent communication |
| | **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | Blazing-fast CLI for prompt iteration and automated red-teaming security scans |
| **Coding & Benchmarks** | **SWE-bench** | [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench) (Princeton/OpenAI) | Real GitHub issue resolution verified by Docker unit test flips (FAIL $\rightarrow$ PASS) |
| | **OpenHands** | [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | Top open-source autonomous coding agent (EventStream + CodeAct runtime) |
| | **SWE-Agent** | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) (Princeton) | Pioneer of Agent-Computer Interface (ACI) with paginated viewing and line-level editing |
| | **OSWorld** | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) (HKU/Princeton) | Real Ubuntu OS multi-modal GUI + CLI cross-app (Office/Chrome/Terminal) evaluation |
| | **Terminal-Bench** | [princeton-nlp/intercode](https://github.com/princeton-nlp/intercode) (Princeton/Berkeley) | Linux Bash terminal sysadmin, troubleshooting & self-correction on execution feedback |
| **Domain Benchmarks** | **VitaBench** | [meituan-longcat](https://github.com/meituan-longcat) (Meituan) | 3D POMDP life services complexity modeling, 66 tools, $\text{Pass}^4$ stress testing |
| | **TAU-bench** | [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) (Stanford/Sierra) | Dynamic customer service benchmark with sandbox DB transaction rollback checks |
| | **GAIA** | [gaia-benchmark](https://huggingface.co/spaces/gaia-benchmark/leaderboard) (Meta/HF) | Multi-modal, multi-step complex general assistant long-horizon tasks (Reverse Turing Test) |
| | **BFCL** | [Gorilla-LLM/BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) (UC Berkeley) | Authoritative tool calling & parallel function calling leaderboard |

---

## 🐱 Spotlight: Meituan LongCat Research Series

We provide in-depth analysis and tracking of the Meituan LongCat team's frontier research:

| Project / Paper | Category | Core Contribution & Eval Significance | Links |
| :--- | :---: | :--- | :--- |
| **VitaBench** | Benchmark | 3D POMDP task complexity modeling, 66-tool dependency graph, and $\text{Pass}^4$ stress testing | [Deep Dive](./docs/07-benchmark-schemas-and-cases.md#四-美团-vitabench生活服务复杂交互评测基准) |
| **LongCat-Next** | Paper | *Lexicalizing Modalities as Discrete Tokens*: Native unified multimodal discrete autoregression | [Paper (arXiv:2603.27538)](https://arxiv.org/pdf/2603.27538) · [GitHub Repo](https://github.com/meituan-longcat/LongCat-Next) |
| **LongCat-Flash** | Tech Report | Ultra-low latency online inference architecture, MoE routing, and long-context KV compression | [Paper (arXiv:2509.01322)](https://arxiv.org/abs/2509.01322) |

---

## 📚 Table of Contents

- [**01. 5 Core Dilemmas & EDD**](./docs/01-dilemmas-and-edd.md): Solving non-determinism, invisible processes, benchmark contamination, and judge biases.
- [**02. Core Metrics & Weapons**](./docs/02-general-weapons.md): Accuracy, BLEU, BERTScore, Position-Swap, and LLM-as-a-Judge rubrics.
- [**03. Model Selection & TCO**](./docs/03-model-selection.md): Capability profiling and hierarchical model routing.
- [**04. Component Evaluation**](./docs/04-component-eval.md): RAG precision/recall/faithfulness, tool hallucination defense, planning reflection errors.
- [**05. 4 Core Engineering Dimensions**](./docs/05-core-quality-dimensions.md): RAG effectiveness, prompt perturbation, schema integrity & API 500 fallbacks.
- [**06. System Integration**](./docs/06-system-integration.md): 5-tier trajectory matching, dynamic multi-turn user simulation, and multi-agent ablation studies.
- [**07. Case Studies & Schemas**](./docs/07-benchmark-schemas-and-cases.md): SWE-bench, OSWorld, Terminal-Bench, Meituan LongCat, TAU-bench, and GAIA.
- [**08. Autonomous Coding Agents**](./docs/08-autonomous-coding-agents.md): Deep dive into OpenHands and SWE-Agent ACI architectures.
- [**09. Release Gates & Observability**](./docs/09-release-and-ops.md): 5 release gates, canary deployments, and data flywheel.
- [**10. Evaluation Platforms & Architecture**](./docs/10-awesome-tools-and-frameworks.md): OpenCompass, LM-Evaluation-Harness, and 5-layer platform architecture.
- [**11. 23 Interview Flashcards**](./docs/11-interview-cards.md): High-frequency interview Q&A.

---

## ⚡ Quick Start

```bash
# 1. Tool calling & negative hallucination test
python evals/tool_eval_demo.py

# 2. RAG two-stage precision & faithfulness test
python evals/rag_eval_demo.py

# 3. Dynamic User Simulator with goal shifts
python evals/user_simulator_demo.py

# 4. Position-Swap debiased LLM judge
python evals/swap_judge_demo.py

# 5. Prompt perturbation, JSON Schema & API 500 fallback test
python evals/robustness_and_fallback_demo.py
```

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
