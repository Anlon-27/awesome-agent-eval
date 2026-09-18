# 10. 全球权威基准深度拆解与标准数据结构 (Benchmark Schemas & Datasets)

工业界评估 Agent 时，如果脱离了业界公认的权威基准，评测结论将失去横向对比的说服力。
本章系统拆解全球四大顶级基准：**SWE-bench**（自主编程）、**OSWorld**（操作系统多模态）、**Terminal-Bench**（命令行运维）与**美团 VitaBench**（生活服务三维 POMDP），并提供标准化样本数据结构（JSON Schemas）与判定规则。

---

## 🏆 一、 全球四大核心 Agent Benchmark 全景对比

| 评测基准 | 主导机构 / 论文 | 核心场景与被测环境 | 核心判定机制与黄金标准 |
| :--- | :--- | :--- | :--- |
| **SWE-bench** | 普林斯顿 / OpenAI | 真实 GitHub 开源仓库 Issue 代码修复 | Docker 沙箱中运行 Unit Test（断言测试用例从 Fail 翻转为 Pass） |
| **OSWorld** | 港大 / 普林斯顿 | 真实 Ubuntu 桌面环境多模态 GUI + CLI 操作 | 跨应用（Chrome、LibreOffice、VS Code）物理状态变更断言 |
| **Terminal-Bench** | 普林斯顿 (InterCode) | Linux 终端 Bash 运维与网络排错 | 命令行标准输出（Stdout/Stderr）与错误自纠偏验证 |
| **VitaBench** | 美团 (LongCat 团队) | 外卖、到店、出行等复杂生活服务 | 三维 POMDP 复杂度建模、66 工具依赖图与 `Pass^4` 严苛抗抖动压测 |

---

## 💻 二、 案例专题一：SWE-bench (代码修复黄金定级赛)

* 📄 **论文**：[*SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (ICLR 2024)*](https://arxiv.org/abs/2310.06770)
* 🐙 **官方仓库**：[`princeton-nlp/SWE-bench`](https://github.com/princeton-nlp/SWE-bench)
* 🌟 **行业地位**：**AI 软件工程与自主代码 Agent 全球公认的唯一“黄金定级赛”！**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🌟 SWE-bench 三大版本矩阵                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. SWE-bench Full (2,294 题) ➔ 涵盖 12 个大型 Python 仓库的真实历史 Issue    │
│ 2. SWE-bench Lite (300 题)   ➔ 精简高频子集，用于算法团队高频快速迭代        │
│ 3. SWE-bench Verified (500 题) ➔ OpenAI 人工专家全面清洗去噪后的权威终极榜单 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📋 标准样本数据结构（SWE-bench Instance Schema）：

```json
{
  "instance_id": "django__django-11099",
  "repo": "django/django",
  "base_commit": "4dfa98e82d1c68f9a2d3b2591638ec8b",
  "problem_statement": "UsernameValidator allows trailing newline in usernames.\n\nDescription:\nASCIIUsernameValidator and UnicodeUsernameValidator accept usernames with a trailing newline...",
  "hints_text": "Discussion and PR comments from maintainers...",
  "created_at": "2019-03-24T18:22:04Z",
  "patch": "diff --git a/django/contrib/auth/validators.py b/django/contrib/auth/validators.py\n--- a/django/contrib/auth/validators.py\n+++ b/django/contrib/auth/validators.py\n@@ -7,7 +7,7 @@\n-    regex = r'^[\\w.@+-]+$'\n+    regex = r'^[\\w.@+-]+\\Z'",
  "test_patch": "diff --git a/tests/auth_tests/test_validators.py b/tests/auth_tests/test_validators.py...",
  "version": "3.0",
  "FAIL_TO_PASS": [
    "tests.auth_tests.test_validators.ASCIIUsernameValidatorTest.test_ascii_validator_trailing_newline",
    "tests.auth_tests.test_validators.UnicodeUsernameValidatorTest.test_unicode_validator_trailing_newline"
  ],
  "PASS_TO_PASS": [
    "tests.auth_tests.test_validators.ASCIIUsernameValidatorTest.test_valid_usernames",
    "tests.auth_tests.test_validators.UnicodeUsernameValidatorTest.test_valid_usernames"
  ],
  "environment_setup_commit": "4dfa98e82d1c68f9a2d3b2591638ec8b"
}
```

#### ⚖️ 核心判定规则：
* **FAIL_TO_PASS 列表**：在 Agent 修改代码应用 Patch 后，列表中所有原本失败的测试用例必须 **100% 变绿（PASS）**；
* **PASS_TO_PASS 列表**：列表中所有原本通过的历史回归测试用例，**绝对不允许被破坏（必须保持 PASS）**。

---

## 🖥️ 三、 案例专题二：OSWorld (真实操作系统多模态基准)

* 📄 **论文**：[*OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Operating Systems (NeurIPS 2024)*](https://arxiv.org/abs/2404.07972)
* 🐙 **官方仓库**：[`xlang-ai/OSWorld`](https://github.com/xlang-ai/OSWorld)
* 🌟 **行业地位**：全球首个**全功能真实计算机操作系统（Ubuntu OS）多模态 GUI + CLI 智能体评测基准**。

### 📋 标准样本数据结构（OSWorld Task Schema）：

```json
{
  "id": "7f8b9c2a-calc-chart-001",
  "instruction": "Open 'sales.csv' on Desktop in LibreOffice Calc, create a 3D bar chart of Q1-Q4 revenue, and save it as 'chart.pdf' in Documents.",
  "domain": "office",
  "app": "libreoffice_calc",
  "initial_state": {
    "files": [
      {
        "path": "/home/user/Desktop/sales.csv",
        "source": "s3://osworld-benchmark/data/sales_2026.csv"
      }
    ],
    "apps_to_open": []
  },
  "evaluation": {
    "evaluator_type": "file_and_content_check",
    "target_file": "/home/user/Documents/chart.pdf",
    "expected_properties": {
      "format": "pdf",
      "page_count": 1,
      "contains_chart": true,
      "chart_type": "bar_3d"
    }
  }
}
```

---

## ⌨️ 四、 案例专题三：Terminal-Bench (命令行与终端 Agent 基准)

* 📄 **代表基准**：[`princeton-nlp/intercode`](https://github.com/princeton-nlp/intercode) / **Terminal-Bench**
* 🌟 **行业地位**：评估 Agent 在 **Linux 命令行终端（Bash / Shell）** 环境下自主运维、网络排错与系统管理的标准基准。

### 📋 标准样本数据结构（Terminal-Bench Schema）：

```json
{
  "task_id": "intercode-bash-042",
  "instruction": "Find all files in /var/log modified in the last 24 hours containing 'ERROR' and save their absolute paths to /tmp/error_files.txt",
  "environment": "docker-ubuntu-22.04",
  "initial_setup": "bash setup_logs.sh",
  "gold_commands": "find /var/log -mtime -1 -type f -exec grep -l 'ERROR' {} + > /tmp/error_files.txt",
  "eval_script": "bash verify_output.sh",
  "expected_state": {
    "target_file": "/tmp/error_files.txt",
    "file_exists": true,
    "non_empty": true
  }
}
```

---

## 🐱 五、 案例专题四：美团龙猫 (Meituan LongCat) 全景前沿体系

### 1. 美团 VitaBench：生活服务复杂交互评测基准
* 📄 **核心定位**：解决学术 Benchmark 过于“玩具化”的痛点，构建首个贴近真实复杂生活场景的 Agent 交互与决策评测环境。
* 🍽️ **核心场景**：外卖点餐、餐厅到店、酒旅出行三大高复杂度生活服务。

### 📋 标准样本数据结构（VitaBench Task Package）：

```json
{
  "task_id": "VITABENCH-FOOD-008",
  "environment": {
    "merchant_id": "poi_98712",
    "merchant_name": "川味小馆",
    "menu": [
      { "item_id": 101, "name": "麻婆豆腐", "price": 38, "stock": 5 },
      { "item_id": 102, "name": "水煮鱼", "price": 88, "stock": 2 }
    ],
    "delivery_slots": ["18:30", "19:00", "19:30"]
  },
  "user_goal_card": {
    "hidden_goal": "点一份麻婆豆腐",
    "budget": 50,
    "delivery_time": "19:00前送达",
    "dynamic_change": "第3轮中途将'微辣'改成'完全不辣'"
  },
  "evaluation_rubric": [
    "最终商品必须是麻婆豆腐",
    "口味必须是不辣 (成功处理改口)",
    "总金额 <= 50 元",
    "送达时间 <= 19:00",
    "下单前必须向用户复述关键信息并请求确认"
  ]
}
```

### 2. LongCat 系列前沿成果：
* **LongCat-Next**：[*Lexicalizing Modalities as Discrete Tokens (arXiv:2603.27538)*](https://arxiv.org/pdf/2603.27538) · [GitHub Repo](https://github.com/meituan-longcat/LongCat-Next)；
* **LongCat-Flash**：[*High-Concurrency Low-Latency Inference (arXiv:2509.01322)*](https://arxiv.org/abs/2509.01322)。

---

## 🏛️ 六、 其他权威基准速查

* **TAU-bench** ([`sierra-research/tau-bench`](https://github.com/sierra-research/tau-bench))：航空公司退改签、电商退货退款等带真实数据库事务回滚的智能客服场景；
* **GAIA** ([Leaderboard](https://huggingface.co/spaces/gaia-benchmark/leaderboard))：通用个人 AI 助手长任务综合基准（反向图灵测试）；
* **BFCL** ([Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html))：UC 伯克利 Tool Calling / Function Calling 权威排行榜。
