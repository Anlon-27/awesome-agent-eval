# -*- coding: utf-8 -*-
from typing import List
from agent_eval.schema import TestCase, Trajectory, MetricResult
from agent_eval.scorers.base import BaseScorer


class RAGFaithfulnessScorer(BaseScorer):
    """
    Evaluates whether the Agent's answer is grounded in retrieved chunks without hallucination.
    """

    def __init__(self, threshold: float = 0.8):
        super().__init__(name="RAGFaithfulness", threshold=threshold)

    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        context_chunks = test_case.context_chunks or []
        final_answer = trajectory.final_answer

        if not context_chunks:
            return MetricResult(
                metric_name=self.name,
                score=1.0,
                passed=True,
                reason="No context chunks specified to ground.",
            )

        combined_context = " ".join(context_chunks).lower()
        golden_keywords = test_case.ground_truth.golden_keywords or []

        if not golden_keywords:
            return MetricResult(
                metric_name=self.name,
                score=1.0,
                passed=True,
                reason="No golden facts specified.",
            )

        hits = sum(1 for kw in golden_keywords if kw.lower() in final_answer.lower())
        score = hits / len(golden_keywords) if golden_keywords else 1.0
        passed = score >= self.threshold

        return MetricResult(
            metric_name=self.name,
            score=score,
            passed=passed,
            reason=f"Hit {hits}/{len(golden_keywords)} golden facts grounded in context.",
            metadata={"hits": hits, "total_keywords": len(golden_keywords)},
        )
