# -*- coding: utf-8 -*-
from typing import List
from agent_eval.schema import TestCase, Trajectory, MetricResult
from agent_eval.scorers.base import BaseScorer


class TrajectoryMatchingScorer(BaseScorer):
    """
    Evaluates Agent trajectory according to the 5-Tier rubric (L1 Perfect to L5 Fatal).
    Detects infinite action loops and calculates effective step ratio.
    """

    def __init__(self, threshold: float = 0.8):
        super().__init__(name="TrajectoryMatching", threshold=threshold)

    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        steps = trajectory.steps
        total_steps = len(steps)

        # 1. Check for infinite loops (Action repeated >= 3 times sequentially)
        actions = [s.action.name for s in steps if s.action]
        for i in range(len(actions) - 2):
            if actions[i] == actions[i+1] == actions[i+2]:
                return MetricResult(
                    metric_name=self.name,
                    score=0.0,
                    passed=False,
                    reason=f"L5 Fatal failure: Infinite action loop detected on '{actions[i]}'.",
                )

        expected_tools = test_case.ground_truth.expected_tools or []
        expected_names = [t.name for t in expected_tools]

        if not expected_names and not actions:
            return MetricResult(
                metric_name=self.name,
                score=1.0,
                passed=True,
                reason="L1 Perfect: Correctly completed without superfluous tool calls.",
            )

        if actions == expected_names:
            min_steps = test_case.ground_truth.min_steps or len(expected_names)
            step_ratio = min_steps / max(total_steps, 1)
            score = 1.0 if step_ratio >= 0.9 else 0.8
            tier = "L1 Perfect" if score == 1.0 else "L2 Valid Alternative"
            return MetricResult(
                metric_name=self.name,
                score=score,
                passed=score >= self.threshold,
                reason=f"{tier}: Tool sequence matched exactly. Effective step ratio: {step_ratio:.2f}",
                metadata={"step_ratio": step_ratio},
            )

        # If tools don't match exactly but contains all expected
        if all(exp in actions for exp in expected_names):
            return MetricResult(
                metric_name=self.name,
                score=0.6,
                passed=0.6 >= self.threshold,
                reason="L3 Recovered with retries: Completed required tools with detours.",
            )

        return MetricResult(
            metric_name=self.name,
            score=0.1,
            passed=False,
            reason=f"L4 Deviated: Actions {actions} failed to complete {expected_names}.",
        )
