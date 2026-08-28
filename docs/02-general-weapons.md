# 02. NLP 与 LLM 核心度量指标体系与开源库 (Evaluation Metrics & Libraries)

在智能体与大模型评测中，针对不同任务形态（分类、抽取、翻译、摘要、开放式生成），必须科学选用**确定性代码度量（Exact / String Overlap）**、**语义表征度量（Embedding / BERTScore）** 与 **智能裁判量规（LLM-as-a-Judge）**。

---

## 📊 一、 核心度量指标全景速查矩阵

| 指标名称 | 计算原理与数学公式 | 适用场景 | 官方开源库 / 对应 GitHub |
| :--- | :--- | :--- | :--- |
| **Accuracy (准确率)** | $\text{Acc} = \frac{TP + TN}{TP + TN + FP + FN}$（预测对的样本比例） | 分类、单选/多选题 (MMLU) | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **Exact Match (EM)** | $\text{EM} = \mathbb{I}(\text{normalize}(\hat{y}) == \text{normalize}(y))$（100% 严格一致） | 问答抽取 (SQuAD)、工具名、状态码 | [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **F1 Score** | $F_1 = 2 \cdot \frac{P \cdot R}{P + R}$（Token 级别的精确率与召回率调和平均） | 槽位抽取、信息提取、命名实体识别 | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`seqeval`](https://github.com/chakki-works/seqeval) |
| **BLEU (1~4)** | 基于 Modified n-gram 匹配精确率，带简短惩罚因子（Brevity Penalty, BP） | 机器翻译、代码生成 (HumanEval) | [`nltk.translate.bleu_score`](https://github.com/nltk/nltk) / [`sacrebleu`](https://github.com/mjpost/sacrebleu) |
| **ROUGE (1/2/L)** | 基于最长公共子序列（LCS）的召回率导向度量 | 文本摘要、长文档提炼、新闻总结 | [`google-research/rouge`](https://github.com/google-research/google-research/tree/master/rouge) / [`rouge-score`](https://github.com/google-research/google-research) |
| **BERTScore** | 计算候选句与参考句在预训练模型（如 RoBERTa）词向量空间中的最大余弦相似度 | 开放式问答、释义生成、语义相似度 | [`Tiiiger/bert_score`](https://github.com/Tiiiger/bert_score) *(ICLR 2020)* |
| **BLEURT** | 基于 BERT 并在合成语料与人类打分上微调的端到端学习型文本质量度量 | 深度语义对齐、高质量机器翻译评测 | [`google-research/bleurt`](https://github.com/google-research/bleurt) *(ACL 2020)* |
| **Perplexity (PPL)** | $\text{PPL}(W) = \exp\left(-\frac{1}{N}\sum \log P(w_i \mid w_{<i})\right)$（困惑度/混乱度） | 语言模型基础建模能力、流畅度度量 | [`huggingface/transformers`](https://github.com/huggingface/transformers) |
| **NDCG@k / MRR** | 归一化折损累计增益（NDCG）与平均倒数排名（MRR） | RAG 知识检索切片排序质量、搜索召回 | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`ranx`](https://github.com/AmenDa/ranx) |

---

## 🔍 二、 核心指标计算原理与代码实操

### 1. BERTScore：攻克传统 BLEU/ROUGE 的“同义词盲区”
* **传统指标痛点**：BLEU 和 ROUGE 依赖字面词重叠，当模型输出同义词时（如“北京天气非常炎热” vs “帝都气候酷暑难耐”），字面重叠为 0，BLEU 得分极低！
* **BERTScore 解决机制**：
  * 利用 Contextual Embedding 计算每个 Token 与参考句中所有 Token 的最大余弦相似度，生成精确率（$P_{\text{BERT}}$）、召回率（$R_{\text{BERT}}$）与 $F_{\text{BERT}}$；
  * **代码调用示例**：
    ```python
    from bert_score import score

    cands = ["北京天气非常炎热"]
    refs = ["帝都气候酷暑难耐"]
    P, R, F1 = score(cands, refs, lang="zh", verbose=False)
    print(f"BERTScore F1: {F1.mean().item():.4f}")  # 得分通常高达 0.85+
    ```

---

## ⚖️ 三、 比较式评估 (Comparative Evaluation)

无论是人类专家还是大语言模型，做“A 与 B 相对比较”都远比给单个输出打“绝对 1-5 分”更可靠。

### 消除“首位偏差 (First-Position Bias)”的标准工程手段：
* **Position Swap（位置对调双盲法）**：
  * 第 1 轮：模型 1 作为 Option A，模型 2 作为 Option B；
  * 第 2 轮：模型 2 作为 Option A，模型 1 作为 Option B；
  * **仅当两次打分一致时才计入胜负，出现冲突则判定为 Tie（平局）**。

---

## 🤖 四、 LLM-as-a-Judge（大模型充当智能裁判）

使用能力更强的模型（如 GPT-4o, Claude 3.7 Sonnet, DeepSeek-V3），按照预定义的**评分量规（Scoring Rubrics）**对开放式输出打分。

### ⚠️ 裁判模型的三大固有偏见与治理：
1. **自我偏好 (Self-bias)**：裁判模型偏爱自己生成的表达风格 ➔ **治理**：采用多裁判交叉投票（Multi-Judge Consensus）；
2. **首位偏差 (First-position bias)** ➔ **治理**：执行 Position Swap；
3. **冗长偏差 (Verbosity bias)**：偏好更长更客套的废话 ➔ **治理**：在 Rubric 中明确惩罚无效冗余信息。
