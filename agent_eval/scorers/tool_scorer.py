# -*- coding: utf-8 -*-
from typing import Dict, Any, List
from agent_eval.schema import TestCase, Trajectory, MetricResult
from agent_eval.scorers.base import BaseScorer


class ToolPrecisionScorer(BaseScorer):
    """
    Evaluates tool selection precision, argument alignment, and negative anti-hallucination.
    """

    def __init__(self, threshold: float = 1.0):
        super().__init__(name="ToolPrecision", threshold=threshold)

    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        expected = test_case.ground_truth.expected_tools or []
        actual = trajectory.tools_called

        # 1. Negative Case: Expecting no tool calls (pure chat/conversational query)
        if not expected:
            if not actual:
                return MetricResult(
                    metric_name=self.name,
                    score=1.0,
                    passed=True,
                    reason="Correctly refrained from calling tools on non-tool input.",
                )
            else:
                hallucinated = [t.name for t in actual]
                return MetricResult(
                    metric_name=self.name,
                    score=0.0,
                    passed=False,
                    reason=f"Tool Hallucination! Unexpected tools invoked: {hallucinated}",
                )

        # 2. Positive Case: Expected tool calls
        if not actual:
            return MetricResult(
                metric_name=self.name,
                score=0.0,
                passed=False,
                reason=f"Missing tool call. Expected: {[t.name for t in expected]}",
            )

        exp_tool = expected[0]
        act_tool = actual[0]

        if exp_tool.name != act_tool.name:
            return MetricResult(
                metric_name=self.name,
                score=0.0,
                passed=False,
                reason=f"Tool mismatch: expected '{exp_tool.name}', got '{act_tool.name}'",
            )

        # Check expected arguments
        missing_args = []
        mismatched_args = []
        for k, v in exp_tool.arguments.items():
            if k not in act_tool.arguments:
                missing_args.append(k)
            elif act_tool.arguments[k] != v:
                mismatched_args.append(f"{k}: expected {v} != got {act_tool.arguments[k]}")

        if missing_args or mismatched_args:
            reasons = []
            if missing_args:
                reasons.append(f"Missing required args: {missing_args}")
            if mismatched_args:
                reasons.append(f"Argument value mismatches: {mismatched_args}")
            return MetricResult(
                metric_name=self.name,
                score=0.5,
                passed=False,
                reason="; ".join(reasons),
            )

        return MetricResult(
            metric_name=self.name,
            score=1.0,
            passed=True,
            reason=f"Tool '{act_tool.name}' and all arguments matched perfectly.",
        )
