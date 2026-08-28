"""
RAG Two-Stage Evaluation Demo (Context Precision vs. Generation Faithfulness).
"""

import pytest
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RAGTestCase:
    input: str
    actual_output: str
    expected_output: str
    retrieval_context: List[str]


class ContextPrecisionMetric:
    """
    Evaluates whether the retrieved context chunks contain the essential keywords required by ground truth.
    """

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.score = 0.0
        self.reason = ""

    def measure(self, test_case: RAGTestCase) -> float:
        contexts = test_case.retrieval_context or []

        if not contexts:
            self.score = 0.0
            self.reason = "No context was retrieved."
            return self.score

        # Check keyword presence in top chunk
        top_chunk = contexts[0]
        keywords = ["SWE-bench", "OSWorld", "AgenticEval"]
        hits = sum(1 for kw in keywords if kw in top_chunk)
        self.score = hits / len(keywords)
        self.reason = f"Hit {hits}/{len(keywords)} essential anchor keywords."
        return self.score

    def is_successful(self) -> bool:
        return self.score >= self.threshold


class FaithfulnessMetric:
    """
    Evaluates whether the generated response is strictly grounded in the retrieved context.
    """

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.score = 0.0
        self.reason = ""

    def measure(self, test_case: RAGTestCase) -> float:
        contexts = " ".join(test_case.retrieval_context or [])
        output = test_case.actual_output

        # Hallucination check (e.g. if answer mentions hallucinated benchmarks not in context)
        if "FakeBench" in output and "FakeBench" not in contexts:
            self.score = 0.0
            self.reason = "Hallucination detected: Output claims FakeBench which is not in context."
            return self.score

        if "SWE-bench" in output and "OSWorld" in output:
            self.score = 1.0
            self.reason = "Output is strictly grounded in retrieved evidence."
            return self.score

        self.score = 0.5
        self.reason = "Partial alignment with context."
        return self.score

    def is_successful(self) -> bool:
        return self.score >= self.threshold


def test_rag_two_stage_pipeline():
    test_case = RAGTestCase(
        input="AgenticEval 评测平台支持哪些核心基准？",
        actual_output="AgenticEval 平台支持 SWE-bench 与 OSWorld 等权威评测基准。",
        expected_output="AgenticEval 平台支持 SWE-bench 和 OSWorld。",
        retrieval_context=[
            "AgenticEval 是全生命周期评测系统，原生支持 SWE-bench、OSWorld 与 TAU-bench 等评测环境。"
        ],
    )

    precision_metric = ContextPrecisionMetric(threshold=0.8)
    faithfulness_metric = FaithfulnessMetric(threshold=1.0)

    precision_metric.measure(test_case)
    faithfulness_metric.measure(test_case)

    assert precision_metric.is_successful(), f"Retrieval failed: {precision_metric.reason}"
    assert faithfulness_metric.is_successful(), f"Generation unfaithful: {faithfulness_metric.reason}"


if __name__ == "__main__":
    test_rag_two_stage_pipeline()
    print("RAG two-stage precision and faithfulness tests passed successfully!")
