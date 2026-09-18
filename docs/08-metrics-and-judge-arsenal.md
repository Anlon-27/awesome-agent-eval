# 08. 核心度量衡与裁判武器库：确定性断言、NLP 度量与双盲 LLM Judge

在智能体与大模型评测中，针对不同任务形态（分类、抽取、工具调用、多步长文生成），必须科学选用**确定性代码度量（Deterministic Assertions）**、**语义向量度量（BERTScore/NDCG）** 与 **智能裁判量规（LLM-as-a-Judge）**。

---

## 📊 一、 核心度量指标全景速查矩阵

| 指标名称 | 计算原理与数学公式 | 适用场景 | 官方开源库 / 对应 GitHub |
| :--- | :--- | :--- | :--- |
| **Accuracy (准确率)** | `Acc = (TP + TN) / Total`（预测对的样本比例） | 分类、单选/多选题 (MMLU) | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **Exact Match (EM)** | `EM = 1 if pred == target else 0`（100% 严格一致） | 问答抽取 (SQuAD)、工具名、状态码 | [`huggingface/evaluate`](https://github.com/huggingface/evaluate) |
| **F1 Score** | `F1 = 2 * (P * R) / (P + R)`（Token 级别的精确率与召回率调和平均） | 槽位抽取、信息提取、命名实体识别 | [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) / [`seqeval`](https://github.com/chakki-works/seqeval) |
| **BLEU (1~4)** | 基于 Modified n-gram 匹配精确率，带简短惩罚因子（Brevity Penalty, BP） | 机器翻译、代码生成 (HumanEval) | [`nltk.translate.bleu_score`](https://github.com/nltk/nltk) / [`sacrebleu`](https://github.com/mjpost/sacrebleu) |
| **ROUGE (1/2/L)** | 基于最长公共子序列（LCS）的召回率导向度量 | 文本摘要、长文档提炼、新闻总结 | [`google-research/rouge`](https://github.com/google-research/google-research/tree/master/rouge) |
| **BERTScore** | 计算候选句与参考句在词向量空间中的最大余弦相似度 | 开放式问答、释义生成、语义相似度 (**攻克同义词盲区**) | [`Tiiiger/bert_score`](https://github.com/Tiiiger/bert_score) *(ICLR 2020)* |
| **NDCG@k / MRR** | 归一化折损累计增益（NDCG）与平均倒数排名（MRR） | RAG 知识检索切片排序质量、搜索召回 | [`ranx`](https://github.com/AmenDa/ranx) / [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) |

---

## 🔍 二、 核心语义指标原理：BERTScore 如何攻克同义词盲区？

* **传统指标痛点**：BLEU 和 ROUGE 依赖严格的字面词重叠。当模型输出高水平同义词时（如“北京天气非常炎热” vs “帝都气候酷暑难耐”），字面重叠为 0，BLEU 得分极低！
* **BERTScore 机制**：利用 Contextual Embedding 计算每个 Token 与参考句中所有 Token 的最大余弦相似度，生成精确率（P_BERT）、召回率（R_BERT）与 F_BERT；
```python
from bert_score import score

cands = ["北京天气非常炎热"]
refs = ["帝都气候酷暑难耐"]
P, R, F1 = score(cands, refs, lang="zh", verbose=False)
print(f"BERTScore F1: {F1.mean().item():.4f}")  # 得分通常高达 0.85+
```

---

## ⚖️ 三、 比较式评测与消除首位偏差 (Position Swap)

无论是人类专家还是大语言模型，做“A 与 B 相对比较（Pairwise Comparison）”都远比给单个输出打“绝对 1-5 分”更客观稳定。

### 消除“首位偏差 (First-Position Bias)”的标准工程手段：
* **Position Swap（位置对调双盲法）**：
  * 第 1 轮：模型 1 作为 Option A，模型 2 作为 Option B；
  * 第 2 轮：模型 2 作为 Option A，模型 1 作为 Option B；
  * **仅当两次打分一致时才计入胜负，出现冲突则判定为 Tie（平局）**。

### 💻 实战代码：
运行项目中提供的双盲消除偏差裁判脚本：
```bash
python evals/swap_judge_demo.py
```

---

## 🤖 四、 LLM-as-a-Judge 量规编制规范 (Scoring Rubrics)

使用旗舰模型（如 GPT-4o、Claude 3.7 Sonnet、DeepSeek-V3）作为裁判时，**绝不能只给一句“请给上面回答打 1-5 分”的模糊 Prompt**。必须遵循量规（Rubric）工程设计：

### 📋 工业级 5 分制量规示例：
* **5 分 (优秀)**：完全达成用户目标，无任何事实幻觉，步骤简明，逻辑严密；
* **4 分 (良好)**：达成主要目标，包含轻微不影响大局的格式冗余，事实准确；
* **3 分 (及格)**：基本完成任务，但存在 1~2 处微小事实瑕疵或多余步骤；
* **2 分 (差)**：未完成核心任务，或提供了无法核实的事实幻觉；
* **1 分 (灾难)**：严重偏离用户意图，包含危险操作或违背伦理安全约束。
