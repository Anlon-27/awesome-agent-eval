# -*- coding: utf-8 -*-
import time
from typing import List, Callable, Dict, Any
from agent_eval.schema import TestCase, Trajectory, CaseEvaluation, EvalReport
from agent_eval.scorers.base import BaseScorer


class AgentRunner:
    """
    Executes test cases against an Agent callable, records trajectories, and computes scores.
    Supports Pass^k evaluation to assess stochastic stability.
    """

    def __init__(self, scorers: List[BaseScorer], pass_k: int = 1):
        self.scorers = scorers
        self.pass_k = pass_k

    def run_case(self, test_case: TestCase, agent_callable: Callable[[TestCase], Trajectory]) -> CaseEvaluation:
        # If pass_k == 1: standard run
        if self.pass_k == 1:
            trajectory = agent_callable(test_case)
            results = [scorer.measure(test_case, trajectory) for scorer in self.scorers]
            return CaseEvaluation(test_case=test_case, trajectory=trajectory, metric_results=results)

        # If pass_k > 1: all k runs must pass for the case to pass
        all_passed = True
        latest_trajectory = None
        aggregated_results = []

        for i in range(self.pass_k):
            traj = agent_callable(test_case)
            latest_trajectory = traj
            run_results = [scorer.measure(test_case, traj) for scorer in self.scorers]
            if not all(r.passed for r in run_results):
                all_passed = False
            aggregated_results = run_results  # keep latest

        if not all_passed:
            for r in aggregated_results:
                r.passed = False
                r.reason = f"Failed Pass^{self.pass_k} stability check. Not all {self.pass_k} runs passed."

        return CaseEvaluation(
            test_case=test_case,
            trajectory=latest_trajectory,
            metric_results=aggregated_results,
        )

    def run_suite(
        self,
        suite_name: str,
        test_cases: List[TestCase],
        agent_callable: Callable[[TestCase], Trajectory],
    ) -> EvalReport:
        start_time = time.time()
        case_evaluations = []

        for tc in test_cases:
            res = self.run_case(tc, agent_callable)
            case_evaluations.append(res)

        duration = time.time() - start_time
        total = len(case_evaluations)
        passed = sum(1 for c in case_evaluations if c.passed)
        pass_rate = (passed / total) if total > 0 else 0.0

        return EvalReport(
            suite_name=suite_name,
            total_cases=total,
            passed_cases=passed,
            pass_rate=pass_rate,
            case_evaluations=case_evaluations,
            duration_sec=duration,
        )
