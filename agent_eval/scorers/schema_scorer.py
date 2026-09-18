# -*- coding: utf-8 -*-
import json
from typing import List
from agent_eval.schema import TestCase, Trajectory, MetricResult
from agent_eval.scorers.base import BaseScorer


class SchemaIntegrityScorer(BaseScorer):
    """
    Evaluates JSON structure compliance, required field existence, and absence of markdown codefence pollution.
    """

    def __init__(self, threshold: float = 1.0):
        super().__init__(name="SchemaIntegrity", threshold=threshold)

    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        raw_output = trajectory.final_answer.strip()
        required_fields = test_case.ground_truth.required_fields

        if required_fields is None:
            return MetricResult(
                metric_name=self.name,
                score=1.0,
                passed=True,
                reason="No schema constraints defined for this test case.",
            )

        if not raw_output:
            return MetricResult(
                metric_name=self.name,
                score=0.0,
                passed=False,
                reason="Empty output.",
            )

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as e:
            return MetricResult(
                metric_name=self.name,
                score=0.0,
                passed=False,
                reason=f"Invalid JSON format: {str(e)}",
            )

        if not isinstance(data, dict):
            return MetricResult(
                metric_name=self.name,
                score=0.5,
                passed=False,
                reason=f"Expected JSON object (dict), got {type(data).__name__}",
            )

        missing = [k for k in required_fields if k not in data]
        if missing:
            return MetricResult(
                metric_name=self.name,
                score=0.5,
                passed=False,
                reason=f"Missing required schema fields: {missing}",
            )

        return MetricResult(
            metric_name=self.name,
            score=1.0,
            passed=True,
            reason="JSON schema validated with 100% field compliance.",
        )
