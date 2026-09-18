# -*- coding: utf-8 -*-
import argparse
import os
import sys
from typing import List
from agent_eval.schema import TestCase, GroundTruth, ToolCall, Trajectory, Step
from agent_eval.loader import DatasetLoader
from agent_eval.scorers.tool_scorer import ToolPrecisionScorer
from agent_eval.scorers.schema_scorer import SchemaIntegrityScorer
from agent_eval.scorers.rag_scorer import RAGFaithfulnessScorer
from agent_eval.scorers.trajectory_scorer import TrajectoryMatchingScorer
from agent_eval.runner import AgentRunner
from agent_eval.reporter import ReportGenerator


def mock_agent_dispatch(tc: TestCase) -> Trajectory:
    inst = tc.instruction.lower()
    if "天气" in inst or "weather" in inst:
        return Trajectory(
            steps=[
                Step(
                    step_index=1,
                    thought="User asks for weather. Need to call get_weather.",
                    action=ToolCall(name="get_weather", arguments={"city": "北京", "date": "2026-08-29"}),
                    observation='{"temp": 26, "condition": "Sunny"}',
                )
            ],
            final_answer='{"status": "success", "data": "晴天，26℃"}',
        )
    elif "客服" in inst or "你好" in inst or "hello" in inst:
        return Trajectory(
            steps=[],
            final_answer="您好！我们的在线客服工作时间为周一至周日 9:00 - 21:00。",
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
    elif "外卖" in inst or "点餐" in inst or "麻婆豆腐" in inst:
        return Trajectory(
            steps=[
                Step(
                    step_index=1,
                    thought="用户点餐，麻婆豆腐，中途改口不辣，送达19:00前，预算50以内。",
                    action=ToolCall(name="create_order", arguments={"item_id": 101, "spicy": "不辣", "delivery_time": "19:00"}),
                    observation='{"order_id": "ORD-5541", "status": "CREATED", "total_price": 38}',
                )
            ],
            final_answer='{"order_id": "ORD-5541", "status": "CREATED", "detail": "麻婆豆腐 (不辣)", "total_price": 38}',
        )
    elif "核心目标" in inst or "rag" in inst:
        return Trajectory(
            steps=[],
            final_answer='{"answer": "Agent评测的核心目标是建立可靠的成功量规与度量衡体系，量化自主规划与工具调用的有效性。", "confidence": 0.98}',
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

    # Load test cases from file
    if os.path.exists(args.dataset):
        test_cases = DatasetLoader.load_from_file(args.dataset)
        suite_name = f"Suite: {os.path.basename(args.dataset)}"
    else:
        print(f"Dataset file '{args.dataset}' not found, exiting.")
        sys.exit(1)

    scorers = [
        ToolPrecisionScorer(),
        SchemaIntegrityScorer(),
        RAGFaithfulnessScorer(),
        TrajectoryMatchingScorer(),
    ]

    runner = AgentRunner(scorers=scorers, pass_k=args.pass_k)
    report = runner.run_suite(suite_name=suite_name, test_cases=test_cases, agent_callable=mock_agent_dispatch)

    print(ReportGenerator.to_terminal(report))

    if args.out_markdown:
        with open(args.out_markdown, "w", encoding="utf-8") as f:
            f.write(ReportGenerator.to_markdown(report))
        print(f"\nSaved markdown report to {args.out_markdown}")

    sys.exit(0 if report.pass_rate >= 0.8 else 1)


if __name__ == "__main__":
    main()
