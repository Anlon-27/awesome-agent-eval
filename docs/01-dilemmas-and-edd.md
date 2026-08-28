# 01. Agent 评测的 5 大困境与评估驱动开发 (EDD)

## 🧭 5 阶渐进式学习路线图 (Progressive Learning Roadmap)

```mermaid
flowchart TD
    classDef stageBox fill:#f8fafc,stroke:#3b82f6,stroke-width:2px,rx:8px,ry:8px;
    classDef stepNode fill:#ffffff,stroke:#cbd5e1,stroke-width:1.5px,color:#0f172a;

    subgraph S1["📘 阶段一：认知建立与度量底座 (Foundations)"]
        direction TB
        N1["01. Agent 评测 5 大困境与评估驱动开发 (EDD)"]
        N2["02. 核心指标与武器库: Accuracy / BLEU / BERTScore / LLM Judge"]
        N1 --> N2
    end
    class S1 stageBox;
    class N1,N2 stepNode;

    subgraph S2["⚙️ 阶段二：选型与零件单体测试 (Components)"]
        direction TB
        N3["03. 基模选型四步法、能力画像与 TCO 架构降本"]
        N4["04. 四大核心零件单体评测 (Prompt / RAG / 工具 / 规划)"]
        N5["05. 四大核心工程质量维度 (RAG 效果 / 扰动稳定性 / 返回质量 / 异常兜底)"]
        N3 --> N4 --> N5
    end
    class S2 stageBox;
    class N3,N4,N5 stepNode;

    subgraph S3["🚀 阶段三：系统集成与前沿基准 (System & Benchmarks)"]
        direction TB
        N6["06. 系统级集成评测 (5 档轨迹比对 / 动态 User Simulator / 多 Agent 消融)"]
        N7["07. 全球权威基准拆解与 JSON Schemas (SWE-bench/OSWorld/Terminal/VitaBench)"]
        N8["08. 自主编程智能体专题 (OpenHands 与 SWE-Agent 架构与 ACI 实战)"]
        N6 --> N7 --> N8
    end
    class S3 stageBox;
    class N6,N7,N8 stepNode;

    subgraph S4["🛡️ 阶段四：发布闸门与评测平台 (Production & Platforms)"]
        direction TB
        N9["09. 5 大发布闸门红线、线上 A/B 灰度与数据飞轮"]
        N10["10. 全球主流评测框架 (OpenCompass/LM-Eval) 与评测平台 5 层架构实战"]
        N9 --> N10
    end
    class S4 stageBox;
    class N9,N10 stepNode;

    subgraph S5["💡 阶段五：疑难解答与最佳实践 (FAQs & Best Practices)"]
        direction TB
        N11["11. 核心疑难问题深度解析与工业界避坑最佳实践 FAQ"]
    end
    class S5 stageBox;
    class N11 stepNode;

    S1 ==> S2 ==> S3 ==> S4 ==> S5
```

---

## 1. 为什么传统的软件测试在 Agent 时代失效？

在传统软件测试中，我们习惯于**确定性的输入与输出断言**（`assert response.status_code == 200`、`assert result == expected`）。然而，当被测对象从确定性代码转变为具备自主决策能力的大模型智能体（AI Agent）时，测试开发工程师面临了 **5 大核心困境**：

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 非确定性 (Non-deterministic) ➔ 传统 Pass/Fail 判定失效     │
│ 2. 过程不可见 ➔ 不能只看最终结果，要识别失败模式与发生频率   │
│ 3. 失败面骤增 ➔ 规划、工具、多轮、多 Agent 协作处处是新单点   │
│ 4. Benchmark 数据污染 ➔ 公开榜单虚高，缺乏业务可迁移性       │
│ 5. 裁判模型偏见 ➔ LLM-as-a-Judge 自带自我偏好、位置与长度偏差│
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 核心思想：评估驱动开发 (Evaluation-Driven Development, EDD)

> **“在动手搭建一个 Agent 之前，必须先定义‘怎么样算成功’。”**

类比传统软件工程中的 **TDD（测试驱动开发）**：
* **传统 TDD**：先写 Unit Test ➔ 运行失败 ➔ 编写业务代码 ➔ 测试通过 ➔ 重构；
* **Agent EDD**：先构建 **Golden Testset（黄金基准评测集）** 与 **自动化 Evaluation Pipeline** ➔ 确立 Baseline 分数 ➔ 迭代 Prompt / 微调模型 / 优化工具 ➔ 验证指标提升 ➔ 触发 CI/CD 发布闸门。

```mermaid
flowchart LR
    classDef step fill:#ffffff,stroke:#3b82f6,stroke-width:1.5px,rx:6px,ry:6px;
    A["定义成功量规 (Rubric)"]:::step --> B["构建黄金评测集 (Golden Set)"]:::step
    B --> C["组装自动化 Eval Pipeline"]:::step
    C --> D["迭代 Prompt / 微调模型 / 工具"]:::step
    D --> E["自动化回归评测 & 指标看板"]:::step
    E -->|通过发布闸门| F["线上 A/B 灰度放量"]:::step
    E -->|未达标| D
```

---

## 3. Agent 全生命周期评测主线

评测不是项目发布前临时抱佛脚的补救措施，而是贯穿产品生命周期的四部曲：

```text
选模型 (选型期) ────> 标记进展 (开发期) ────> 决定上线 (发布期) ────> 生产监控 (运行期)
```

1. **选型期**：通过场景反推能力画像，利用私有数据集进行双盲测试，建立 TCO 架构分层；
2. **开发期（组件+集成）**：单体测试 Prompt、RAG、Tool Calling 与 Planning，系统级测试多轮交互与多 Agent 协作；
3. **发布期**：建立包含“功能正确性、零安全漏洞、P95 延迟、Token 成本预算”的 5 大发布闸门；
4. **运行期**：搭建 Logs/Traces/Metrics 可观测性底座，实时监控语义漂移，并将生产 Bad Case 自动回灌评测集形成数据飞轮。
