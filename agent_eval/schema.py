# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json


@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    call_id: Optional[str] = None


@dataclass
class Step:
    step_index: int
    thought: str = ""
    action: Optional[ToolCall] = None
    observation: str = ""


@dataclass
class Trajectory:
    steps: List[Step] = field(default_factory=list)
    final_answer: str = ""
    latency_ms: float = 0.0
    token_usage: Dict[str, int] = field(default_factory=dict)

    @property
    def tools_called(self) -> List[ToolCall]:
        return [step.action for step in self.steps if step.action is not None]


@dataclass
class GroundTruth:
    expected_tools: Optional[List[ToolCall]] = None
    expected_state_diff: Optional[Dict[str, Any]] = None
    golden_keywords: Optional[List[str]] = None
    required_fields: Optional[List[str]] = None
    min_steps: Optional[int] = None
    max_steps: Optional[int] = None


@dataclass
class TestCase:
    task_id: str
    layer: str  # L0, L1, L2, L3, L4
    instruction: str
    ground_truth: GroundTruth
    context_chunks: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricResult:
    metric_name: str
    score: float
    passed: bool
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CaseEvaluation:
    test_case: TestCase
    trajectory: Trajectory
    metric_results: List[MetricResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(m.passed for m in self.metric_results) if self.metric_results else False


@dataclass
class EvalReport:
    suite_name: str
    total_cases: int
    passed_cases: int
    pass_rate: float
    case_evaluations: List[CaseEvaluation] = field(default_factory=list)
    duration_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_name": self.suite_name,
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "pass_rate": round(self.pass_rate, 4),
            "duration_sec": round(self.duration_sec, 2),
            "cases": [
                {
                    "task_id": c.test_case.task_id,
                    "layer": c.test_case.layer,
                    "passed": c.passed,
                    "metrics": [
                        {
                            "name": m.metric_name,
                            "score": m.score,
                            "passed": m.passed,
                            "reason": m.reason,
                        }
                        for m in c.metric_results
                    ],
                }
                for c in self.case_evaluations
            ],
        }
