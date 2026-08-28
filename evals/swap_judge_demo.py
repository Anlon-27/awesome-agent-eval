"""
Position-Swap Debiased LLM-as-a-Judge Implementation.
Eliminates first-position bias by running pairwise evaluations twice with swapped order.
"""

from typing import Tuple, Optional


def mock_llm_judge(candidate_a: str, candidate_b: str) -> str:
    """
    Mock LLM Judge. Returns 'A' if candidate_a is strictly preferred, 'B' otherwise.
    Demonstrates position-sensitive evaluation (concise factual answer wins).
    """
    # A concise and factual answer wins
    if len(candidate_a) < len(candidate_b) and "SWE-bench" in candidate_a:
        return "A"
    return "B"


def evaluate_with_position_swap(model_out_1: str, model_out_2: str) -> str:
    """
    Runs pairwise comparison twice:
    Round 1: model_out_1 as A, model_out_2 as B
    Round 2: model_out_2 as A, model_out_1 as B (Swapped)

    Returns: 'MODEL_1_WINS', 'MODEL_2_WINS', or 'TIE / POSITION_BIAS_DETECTED'
    """
    # Round 1
    winner_round1 = mock_llm_judge(model_out_1, model_out_2)

    # Round 2 (Swapped)
    winner_round2 = mock_llm_judge(model_out_2, model_out_1)

    if winner_round1 == "A" and winner_round2 == "B":
        return "MODEL_1_WINS"
    elif winner_round1 == "B" and winner_round2 == "A":
        return "MODEL_2_WINS"
    else:
        return "TIE / POSITION_BIAS_DETECTED"


def test_swap_judge():
    out1 = "AgenticEval 原生支持 SWE-bench 代码修复基准。"
    out2 = "AgenticEval 是一个非常强大且复杂的智能体系统，不仅能做很多评测任务，还能生成很多自动化报告。"

    verdict = evaluate_with_position_swap(out1, out2)
    assert verdict == "MODEL_1_WINS", f"Expected MODEL_1_WINS, got {verdict}"


if __name__ == "__main__":
    test_swap_judge()
    print("Position-Swap debiased judge test passed successfully!")
