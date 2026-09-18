# -*- coding: utf-8 -*-
import pytest
from agent_eval.schema import TestCase, GroundTruth, ToolCall, Trajectory, Step
from agent_eval.scorers.tool_scorer import ToolPrecisionScorer
from agent_eval.runner import AgentRunner
from agent_eval.reporter import ReportGenerator


def test_agent_runner_single_and_pass_k():
    tc = TestCase(
        task_id="T10",
        layer="L1",
        instruction="Check balance",
        ground_truth=GroundTruth(
            expected_tools=[ToolCall(name="get_balance", arguments={"account_id": "ACC123"})]
        ),
    )

    def reliable_agent(test_case: TestCase) -> Trajectory:
        return Trajectory(
            steps=[Step(step_index=1, action=ToolCall(name="get_balance", arguments={"account_id": "ACC123"}))]
        )

    # 1. Standard run
    runner = AgentRunner(scorers=[ToolPrecisionScorer()], pass_k=1)
    report = runner.run_suite(suite_name="Test Suite", test_cases=[tc], agent_callable=reliable_agent)
    assert report.total_cases == 1
    assert report.passed_cases == 1
    assert report.pass_rate == 1.0

    # 2. Pass^4 run (all 4 runs must pass)
    runner_k4 = AgentRunner(scorers=[ToolPrecisionScorer()], pass_k=4)
    report_k4 = runner_k4.run_suite(suite_name="Pass^4 Suite", test_cases=[tc], agent_callable=reliable_agent)
    assert report_k4.passed_cases == 1
    assert report_k4.pass_rate == 1.0

    # 3. Formatter output
    term_table = ReportGenerator.to_terminal(report_k4)
    assert "PASS" in term_table
    md_content = ReportGenerator.to_markdown(report_k4)
    assert "# 📊 Evaluation Report: Pass^4 Suite" in md_content
