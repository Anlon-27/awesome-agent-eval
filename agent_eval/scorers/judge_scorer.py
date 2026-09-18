# -*- coding: utf-8 -*-
from typing import Dict, Any, Callable, Optional
from agent_eval.schema import TestCase, Trajectory, MetricResult
from agent_eval.scorers.base import BaseScorer


class PositionSwapJudgeScorer(BaseScorer):
    """
    Evaluates pairwise model outputs using Position-Swap to eliminate First-Position Bias.
    """

    def __init__(self, arbiter_fn: Optional[Callable[[str, str, str], str]] = None, threshold: float = 1.0):
        super().__init__(name="PositionSwapJudge", threshold=threshold)
        self.arbiter_fn = arbiter_fn or self._default_mock_arbiter

    def _default_mock_arbiter(self, instruction: str, option_a: str, option_b: str) -> str:
        # Mock arbiter: prefers structured informative responses
        score_a = len(option_a) + (50 if "{" in option_a or "[" in option_a else 0)
        score_b = len(option_b) + (50 if "{" in option_b or "[" in option_b else 0)
        if abs(score_a - score_b) < 10:
            return "TIE"
        return "A" if score_a > score_b else "B"

    def measure_pair(self, instruction: str, output_1: str, output_2: str) -> Dict[str, Any]:
        # Round 1: Model 1 as Option A, Model 2 as Option B
        res1 = self.arbiter_fn(instruction, output_1, output_2)

        # Round 2: Model 2 as Option A, Model 1 as Option B (Position Swapped)
        res2 = self.arbiter_fn(instruction, output_2, output_1)

        # Determine winner
        # In Round 1, 'A' means output_1 won, 'B' means output_2 won.
        # In Round 2, 'A' means output_2 won, 'B' means output_1 won.
        if res1 == "A" and res2 == "B":
            winner = "MODEL_1"
            score = 1.0
            consistent = True
        elif res1 == "B" and res2 == "A":
            winner = "MODEL_2"
            score = 0.0
            consistent = True
        else:
            winner = "TIE_OR_INCONSISTENT"
            score = 0.5
            consistent = False

        return {
            "winner": winner,
            "consistent": consistent,
            "round_1_choice": res1,
            "round_2_choice": res2,
            "score": score,
        }

    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        # Measure against golden reference answer if present
        ref = test_case.ground_truth.golden_keywords or []
        ref_text = " ".join(ref)
        res = self.measure_pair(test_case.instruction, trajectory.final_answer, ref_text)
        return MetricResult(
            metric_name=self.name,
            score=res["score"],
            passed=res["consistent"] and res["score"] >= self.threshold,
            reason=f"Position Swap Winner: {res['winner']} (Consistent: {res['consistent']})",
            metadata=res,
        )
