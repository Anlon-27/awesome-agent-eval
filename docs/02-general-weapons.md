# 02. 三大通用评测武器库

在贯穿 Agent 生命周期的评测中，有三件**跨越选型、开发、发布与监控的通用武器**：

---

## 武器一：基础代码度量（精确匹配与语义相似度）

当 Agent 的输出具有明确标准答案或高度结构化时，**首选代码级确定性度量**。

### 1. 结构化度量（零成本、可完全复现）
* **Exact Match (EM, 精确匹配)**：归一化后字符串完全一致，适用于工具名称、分类标签、枚举状态。
* **JSON Schema 校验**：验证返回的 JSON 键值对类型、必填字段是否完整。
* **Token-level F1 Score**：精确率（Precision）与召回率（Recall）的调和平均数，适用于信息抽取与槽位解析。

### 2. 文本语义度量
* **ROUGE-L**：基于最长公共子序列（LCS），适用于文本摘要评测。
* **BLEU**：基于 n-gram 精确率（带简短惩罚），适用于翻译与结构化转换。
* **Embedding Cosine Similarity**：通过向量余弦相似度粗筛文本语义相关性。

---

## 武器二：比较式评估 (Comparative Evaluation)

认知科学和 LLM 实践证明：**无论是人类专家还是大语言模型，做“A 与 B 相对比较”都远比给单个输出打“绝对 1-5 分”更稳定、更敏感。**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Pairwise Comparison (两两胜率对比) ➔ 离线版本迭代首选    │
│ 2. Elo Rating (等级分体系) ➔ 跨模型批次排行榜 (如 Chatbot Arena) │
│ 3. Bradley-Terry 模型 ➔ 概率化偏好估计                      │
└─────────────────────────────────────────────────────────────┘
```

### 消除“首位偏差 (First-Position Bias)”的标准工程手段：
* **Position Swap（位置对调双盲法）**：
  * 第 1 轮：模型 1 作为 Option A，模型 2 作为 Option B；
  * 第 2 轮：模型 2 作为 Option A，模型 1 作为 Option B；
  * **仅当两次打分一致时才计入胜负，出现冲突则判定为 Tie（平局）**。

---

## 武器三：LLM-as-a-Judge（大模型充当智能裁判）

使用能力更强的模型（如 GPT-4o, Claude 3.7 Sonnet, DeepSeek-V3），按照预定义的**评分量规（Scoring Rubrics）**对开放式输出打分。

### 标准 Judge Prompt 四要素结构：

```jinja2
system:
You are an expert evaluator assessing the performance of an AI Agent.
Evaluate the following response based on the defined Rubrics:

[Rubrics]
1 Poor: Fails to meet constraints, contains hallucinations.
3 Mediocre: Partially answers query, minor inaccuracies.
5 Excellent: Perfectly satisfies all user constraints with high fidelity.

[Output Format]
Output strictly in valid JSON format:
{
  "reasoning": "Step-by-step evaluation analysis...",
  "score": 5
}
user:
Task Input: {{ input }}
Agent Output: {{ output }}
```

### ⚠️ 裁判模型的三大固有偏见与治理：
1. **自我偏好 (Self-bias)**：裁判模型天然偏爱自己生成的表达风格 ➔ **治理**：采用多裁判交叉投票（Multi-Judge Consensus）；
2. **首位偏差 (First-position bias)** ➔ **治理**：执行 Position Swap；
3. **冗长偏差 (Verbosity bias)**：偏好更长、更客套的废话 ➔ **治理**：在 Rubric 中明确惩罚无效冗余信息。
