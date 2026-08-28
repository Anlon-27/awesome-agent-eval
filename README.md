<div align="center">

# 🤖 Awesome Agent Eval (工业级 AI Agent 评测全景体系)

**The Definitive Guide, Methodology & Engineering Toolkit for AI Agent Evaluation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](./README_EN.md) | [简体中文](./README.md) | [📚 体系化指南](./docs/) | [💻 实战代码](./evals/) | [📊 黄金数据集](./datasets/)

</div>

---

## 📖 项目简介 (Introduction)

随着大语言模型从单轮问答演进为具备“自主规划、工具调用、多轮交互、多智能体协作”的 **AI Agent**，传统的确定性软件测试与简单的问答评测已经完全失效。

**Awesome Agent Eval** 旨在构建一个**工业级、端到端、贯穿 Agent 全生命周期（选型 ➔ 零件 ➔ 轨迹 ➔ 发布 ➔ 监控）的权威评测体系与实操框架**。深度覆盖 **RAG 检索效果诊断、提示词扰动鲁棒性、模型结构化返回质量（JSON Schema）与生产级异常兜底容错**，并无缝融合全球前沿框架（**DeepEval、Ragas、OpenHands、SWE-agent**）与权威基准（**SWE-bench、OSWorld、Terminal-Bench、美团龙猫 VitaBench、TAU-bench**）。

---

## 🧭 Agent 评测全生命周期架构图 (Evaluation Landscape)

```mermaid
graph TD
    A["Agent 全生命周期评估驱动开发 (EDD)"] --> B["1. 选型期 (Model Selection)<br/>• 场景反推能力画像与权重配比<br/>• 硬门槛初筛 + TCO 架构分层<br/>• 私有业务数据集双盲测试"]
    A --> C["2. 组件评测 (Component Eval)<br/>• 提示词扰动稳定性与鲁棒性<br/>• RAG 双段法 (Context Precision/Recall vs 忠实度)<br/>• Tool Calling 4 项核对 + 防幻觉反例<br/>• Planning 3 大典型失败模式归因"]
    A --> D["3. 系统集成 (System Eval)<br/>• 任务终态 (Pass@k vs Pass^k)<br/>• 轨迹评测 (5 档严格度比对)<br/>• 动态 User Simulator + 隐藏目标卡<br/>• 多 Agent 协作评测与消融实验"]
    A --> E["4. 发布与运维 (Release & Ops)<br/>• 5 大发布闸门红线 (质量/成本/安全)<br/>• 线上 A/B 测试 (真实业务流量裁决)<br/>• 异常优雅降级 (API 500 兜底与防堆栈泄露)<br/>• Bad Case 回灌离线基准集形成数据飞轮"]
```

---

## 🛠️ 全球前沿 Agent 评测工具与框架生态雷达 (Ecosystem Radar)

| 领域分类 | 核心工具 / 权威基准 | 主导机构 / 仓库 | 核心评测场景与特长 |
| :--- | :--- | :--- | :--- |
| **自主编程 Agent 与代码基准** | **SWE-bench** | [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench) (普林斯顿/OpenAI) | 真实 GitHub Issue 代码修复（以 Docker 沙箱中 Unit Test 翻转为黄金标准） |
| | **OpenHands** | [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | 顶尖自主编程 Agent 框架（EventStream 事件驱动 + CodeAct 代码执行模式） |
| | **SWE-Agent** | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) (普林斯顿大学) | 首个开创 ACI（智能体-计算机接口）的分页查看与行级精准编辑开源智能体 |
| **系统与终端交互基准** | **OSWorld** | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) (港大/普林斯顿) | 真实 Ubuntu 操作系统多模态 GUI + CLI 跨应用（Office/Chrome/Terminal）操作基准 |
| | **Terminal-Bench** | [princeton-nlp/intercode](https://github.com/princeton-nlp/intercode) (普林斯顿/伯克利) | Linux 命令行终端 Bash 自主运维、网络排错与基于错误输出的自我纠错评测 |
| **复杂业务场景基准** | **VitaBench** | [meituan-longcat](https://github.com/meituan-longcat) (美团) | 外卖/到店/出行复杂生活服务三维 POMDP 建模、$\text{Pass}^4$ 严苛抗抖动压测 |
| | **TAU-bench** | [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) (Stanford/Sierra) | 智能客服环境状态验证（真实数据库事务回滚与防越权检查） |
| | **GAIA** | [gaia-benchmark](https://huggingface.co/spaces/gaia-benchmark/leaderboard) (Meta/HF) | 通用个人助手长链路多模态、多步骤文件/代码综合处理基准（反向图灵测试） |
| | **BFCL** | [Gorilla-LLM/BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) (UC 伯克利) | 原生 Tool Calling / Function Calling 权威排行榜与多语言调用评测 |
| **评测框架与断言库** | **DeepEval** | [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | 生产级 Agent 单元测试、G-Eval 自定义量规、CI/CD 集成 (本仓库默认引擎) |
| | **Ragas** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | 专注 RAG 检索质量、生成忠实度与多 Agent 通信交互评估 |
| | **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 高性能 CLI 工具，主打 Prompt 变体对比与红队安全渗透自动化测试 |
| | **Inspect AI** | [UK-AI-Safety-Institute/inspect_ai](https://github.com/UK-AI-Safety-Institute/inspect_ai) | 英国人工智能安全研究所出品，专注模型长链路安全与能力评估 |
| | **DSPy** | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | 斯坦福大学出品，通过自动化 Metric 驱动 Prompt 自动编译与调优 |
| **可观测与 Tracing** | **AgentOps** | [AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops) | 专为 Agent 设计的调用链追踪、死循环检测与 Token 费用分析 |
| | **Phoenix** | [Arize-AI/phoenix](https://github.com/Arize-AI/phoenix) | 完全开源的 LLM/RAG 可观测性平台与 UMAP 语义漂移聚类分析 |

---

## 🐱 前沿聚焦：美团龙猫 (Meituan LongCat) 系列研究

| 研究成果 | 类型 | 核心创新点 / 评测意义 | 链接 |
| :--- | :---: | :--- | :--- |
| **VitaBench** | 评测基准 | 生活服务三维 POMDP 复杂度建模、66 工具依赖图、$\text{Pass}^4$ 严苛压测 | [详细解析](./docs/07-case-studies.md#四-美团-vitabench生活服务复杂交互评测基准) |
| **LongCat-Next** | 顶会论文 | *Lexicalizing Modalities as Discrete Tokens*：原生统一离散多模态自回归架构 | [Paper (arXiv:2603.27538)](https://arxiv.org/pdf/2603.27538) · [GitHub Repo](https://github.com/meituan-longcat/LongCat-Next) |
| **LongCat-Flash** | 技术报告 | 高并发实时业务极致低时延推理、MoE 稀疏优化与长上下文 KV 压缩 | [Paper (arXiv:2509.01322)](https://arxiv.org/abs/2509.01322) |

---

## 📚 体系化深度指南 (Comprehensive Guides)

| 章节 | 核心主题 | 关键要点 |
| :--- | :--- | :--- |
| [**01. 困境与 EDD**](./docs/01-dilemmas-and-edd.md) | Agent 评测 5 大困境与评估驱动开发 | 解决非确定性、过程不可见、数据污染与裁判偏见 |
| [**02. 通用武器库**](./docs/02-general-weapons.md) | 三大通用评测方法与度量衡 | 精确匹配 / 比较评估 (Position Swap) / LLM-as-a-Judge |
| [**03. 基模选型**](./docs/03-model-selection.md) | 选型四步法与 TCO 架构降本 | 场景反推能力画像、旗舰与轻量模型分流架构 |
| [**04. 核心零件评测**](./docs/04-component-eval.md) | Prompt / RAG / 工具 / 规划单体验证 | RAG 忠实度、Tool Calling 防幻觉反例、规划反思错误 |
| [**05. 系统级集成**](./docs/05-system-integration.md) | 轨迹比对、多轮对抗与团队消融 | 5 档轨迹严格度、动态 User Simulator、多 Agent 消融实验 |
| [**06. 发布与运维**](./docs/06-release-and-ops.md) | 5 大发布闸门红线与线上可观测性 | 质量/时延/安全红线、灰度放量、数据飞轮回归闭环 |
| [**07. 前沿案例与数据结构**](./docs/07-case-studies.md) | 权威基准深度拆解与 JSON Schemas | SWE-bench、OSWorld、Terminal-Bench、美团 LongCat、TAU-bench |
| [**08. 高频面试题**](./docs/08-interview-cards.md) | 23 道 Agent 评测核心面试题与答题卡片 | 涵盖概念、方法、指标、工程落地全景解析 |
| [**09. 生态雷达**](./docs/09-awesome-tools-and-frameworks.md) | 全球 18 大 Agent 评测工具与基准矩阵 | 选型对比表、功能矩阵与测试开发团队最佳落地路径 |
| [**10. 自主编程 Agent 专题**](./docs/10-autonomous-coding-agents.md) | OpenHands 与 SWE-Agent 架构深度拆解 | ACI 智能体-计算机接口设计、EventStream 与 SWE-bench 实战 |
| [**11. 四大工程质量维度**](./docs/11-core-quality-dimensions.md) | RAG 效果、提示词鲁棒性、返回质量与异常兜底 | 扰动测试、JSON 结构合规、API 500 优雅降级与熔断防护 |

---

## ⚡ 极速上手：运行自动化评测代码 (Quick Start)

```bash
# 1. 运行工具调用精准度与防幻觉测试
python evals/tool_eval_demo.py

# 2. 运行 RAG 检索段 Context Precision 与生成段 Faithfulness 测试
python evals/rag_eval_demo.py

# 3. 运行多轮动态 User Simulator 交互测试
python evals/user_simulator_demo.py

# 4. 运行消除首位偏差的双盲裁判测试 (Position-Swap Judge)
python evals/swap_judge_demo.py

# 5. 运行提示词扰动鲁棒性、JSON Schema 校验与 API 500 异常兜底测试
python evals/robustness_and_fallback_demo.py
```

---

## 📊 评测数据集模板 (Golden Benchmark Datasets)

本项目在 [`datasets/`](./datasets/) 目录下提供了工业级评测数据集模板：
* [`tool_test_cases.json`](./datasets/tool_test_cases.json)：包含标准工具调用与“不该调工具”的防幻觉反例；
* [`multi_turn_goals.json`](./datasets/multi_turn_goals.json)：包含环境配置、隐藏目标卡与多轮 Rubric 判定标准；
* [`rag_golden_set.json`](./datasets/rag_golden_set.json)：包含知识切片、标准回答与忠实度基准。

---

## 🤝 参与贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！
- 🌟 分享工业界前沿的 Agent 评测论文与 Benchmark；
- 🛠️ 贡献新的 Metric 评测算法与实战代码；
- 📝 优化中英文文档与面试题库。

---

## 📄 开源许可证 (License)

本项目采用 [MIT License](./LICENSE) 协议开源。欢迎自由引用与二次开发，请保留原作者出处！
