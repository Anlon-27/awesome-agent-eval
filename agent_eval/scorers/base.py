# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from agent_eval.schema import TestCase, Trajectory, MetricResult


class BaseScorer(ABC):
    def __init__(self, name: str, threshold: float = 1.0):
        self.name = name
        self.threshold = threshold

    @abstractmethod
    def measure(self, test_case: TestCase, trajectory: Trajectory) -> MetricResult:
        pass
