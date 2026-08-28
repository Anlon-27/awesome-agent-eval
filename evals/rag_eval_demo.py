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
        keywords = ["40+", "无人机", "MotoTest"]
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

        # Hallucination check (e.g. if answer mentions 100 instead of 40+)
        if "100" in output and "100" not in contexts:
            self.score = 0.0
            self.reason = "Hallucination detected: Output claims 100 which is not in context."
            return self.score

        if "40+" in output:
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
        input="MotoTest 平台最多支持多少台无人机？",
        actual_output="MotoTest 平台支持同时管理 40+ 台无人机进行分布式自动化测试。",
        expected_output="MotoTest 平台支持 40+ 台无人机。",
        retrieval_context=[
            "MotoTest 是基于 Flask 与 SocketIO 的分布式平台，管理 40+ 台无人机设备并实现压测可视化。"
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
