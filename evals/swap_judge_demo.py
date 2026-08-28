"""
Position-Swap Debiased LLM-as-a-Judge Implementation.
Eliminates first-position bias by running pairwise evaluations twice with swapped order.
"""

from typing import Tuple, Optional


def mock_llm_judge(candidate_a: str, candidate_b: str) -> str:
    """
    Mock LLM Judge. Returns 'A' if candidate_a is strictly preferred, 'B' otherwise.
    Demonstrates position-sensitive evaluation.
    """
    # A concise and factual answer wins
    if len(candidate_a) < len(candidate_b) and "40+" in candidate_a:
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
    out1 = "MotoTest 支持 40+ 台无人机管理。"
    out2 = "MotoTest 是一个非常强大且复杂的分布式自动化测试系统，不仅能管理许多无人机，还能跑很多自动化脚本。"

    verdict = evaluate_with_position_swap(out1, out2)
    assert verdict == "MODEL_1_WINS", f"Expected MODEL_1_WINS, got {verdict}"


if __name__ == "__main__":
    test_swap_judge()
    print("Position-Swap debiased judge test passed successfully!")
