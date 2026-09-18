# -*- coding: utf-8 -*-
import argparse
import json
import sys
from agent_eval.schema import TestCase, GroundTruth, ToolCall, Trajectory, Step
from agent_eval.scorers.tool_scorer import ToolPrecisionScorer
from agent_eval.scorers.schema_scorer import SchemaIntegrityScorer
from agent_eval.scorers.rag_scorer import RAGFaithfulnessScorer
from agent_eval.scorers.trajectory_scorer import TrajectoryMatchingScorer
from agent_eval.runner import AgentRunner
from agent_eval.reporter import ReportGenerator


def mock_agent_dispatch(tc: TestCase) -> Trajectory:
    # A lightweight mock agent implementation for CLI testing
    inst = tc.instruction.lower()
    if "天气" in inst or "weather" in inst:
        return Trajectory(
            steps=[
                Step(
                    step_index=1,
                    thought="User asks for weather. Need to call get_weather.",
                    action=ToolCall(name="get_weather", arguments={"city": "Beijing", "date": "2026-10-01"}),
                    observation='{"temp": 22, "condition": "Sunny"}',
                )
            ],
            final_answer='{"status": "success", "data": "Sunny, 22C"}',
        )
    elif "你好" in inst or "hello" in inst:
        return Trajectory(
            steps=[],
            final_answer="Hello! How can I assist you today?",
        )
    elif "订票" in inst or "火车" in inst or "train" in inst:
        return Trajectory(
            steps=[
                Step(
                    step_index=1,
                    thought="Need to book a train ticket.",
                    action=ToolCall(name="book_train", arguments={"train_no": "G123", "seat": "second_class"}),
                    observation='{"status": "confirmed"}',
                )
            ],
            final_answer='{"order_id": "T88912", "status": "booked"}',
        )
    return Trajectory(
        steps=[],
        final_answer="Request processed.",
    )


def main():
    parser = argparse.ArgumentParser(description="Awesome Agent Eval CLI")
    parser.add_argument("--dataset", type=str, default="datasets/tool_test_cases.json", help="Path to testset JSON")
    parser.add_argument("--pass-k", type=int, default=1, help="Pass^k repeated runs (default: 1)")
    parser.add_argument("--out-markdown", type=str, default=None, help="Save report as markdown file")
    args = parser.parse_args()

    # Build demo test suite
    test_cases = [
        TestCase(
            task_id="TC-TOOL-001",
            layer="L1",
            instruction="帮我查询北京2026-10-01的天气",
            ground_truth=GroundTruth(
                expected_tools=[ToolCall(name="get_weather", arguments={"city": "Beijing", "date": "2026-10-01"})],
                required_fields=["status", "data"],
            ),
        ),
        TestCase(
            task_id="TC-TOOL-NEG-002",
            layer="L1",
            instruction="你好，讲个笑话吧",
            ground_truth=GroundTruth(
                expected_tools=[],  # Negative case: tool hallucination check
            ),
        ),
        TestCase(
            task_id="TC-PLAN-003",
            layer="L2",
            instruction="帮我订一张G123的二等座火车票",
            ground_truth=GroundTruth(
                expected_tools=[ToolCall(name="book_train", arguments={"train_no": "G123", "seat": "second_class"})],
                required_fields=["order_id", "status"],
            ),
        ),
    ]

    scorers = [
        ToolPrecisionScorer(),
        SchemaIntegrityScorer(),
        TrajectoryMatchingScorer(),
    ]

    runner = AgentRunner(scorers=scorers, pass_k=args.pass_k)
    report = runner.run_suite(suite_name="Agent Eval Standard Suite", test_cases=test_cases, agent_callable=mock_agent_dispatch)

    print(ReportGenerator.to_terminal(report))

    if args.out_markdown:
        with open(args.out_markdown, "w", encoding="utf-8") as f:
            f.write(ReportGenerator.to_markdown(report))
        print(f"\nSaved markdown report to {args.out_markdown}")

    sys.exit(0 if report.pass_rate >= 0.8 else 1)


if __name__ == "__main__":
    main()
