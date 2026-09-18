# -*- coding: utf-8 -*-
import pytest
from agent_eval.schema import (
    TestCase,
    GroundTruth,
    ToolCall,
    Step,
    Trajectory,
)
from agent_eval.scorers.tool_scorer import ToolPrecisionScorer
from agent_eval.scorers.schema_scorer import SchemaIntegrityScorer
from agent_eval.scorers.rag_scorer import RAGFaithfulnessScorer
from agent_eval.scorers.trajectory_scorer import TrajectoryMatchingScorer
from agent_eval.scorers.judge_scorer import PositionSwapJudgeScorer


def test_tool_scorer_positive_match():
    scorer = ToolPrecisionScorer()
    tc = TestCase(
        task_id="T1",
        layer="L1",
        instruction="Check weather",
        ground_truth=GroundTruth(
            expected_tools=[ToolCall(name="get_weather", arguments={"city": "Beijing"})]
        ),
    )
    traj = Trajectory(
        steps=[Step(step_index=1, action=ToolCall(name="get_weather", arguments={"city": "Beijing"}))]
    )
    res = scorer.measure(tc, traj)
    assert res.passed is True
    assert res.score == 1.0


def test_tool_scorer_negative_anti_hallucination():
    scorer = ToolPrecisionScorer()
    tc = TestCase(
        task_id="T2",
        layer="L1",
        instruction="Tell me a joke",
        ground_truth=GroundTruth(expected_tools=[]),
    )
    # Case A: Correctly refrained
    traj_pass = Trajectory(steps=[])
    res_pass = scorer.measure(tc, traj_pass)
    assert res_pass.passed is True
    assert res_pass.score == 1.0

    # Case B: Hallucinated tool call
    traj_fail = Trajectory(
        steps=[Step(step_index=1, action=ToolCall(name="call_uber", arguments={}))]
    )
    res_fail = scorer.measure(tc, traj_fail)
    assert res_fail.passed is False
    assert res_fail.score == 0.0
    assert "Tool Hallucination" in res_fail.reason


def test_schema_scorer_valid_and_invalid():
    scorer = SchemaIntegrityScorer()
    tc = TestCase(
        task_id="T3",
        layer="L1",
        instruction="Generate user profile",
        ground_truth=GroundTruth(required_fields=["name", "age"]),
    )
    # Valid
    traj_valid = Trajectory(final_answer='{"name": "Alice", "age": 28}')
    res_valid = scorer.measure(tc, traj_valid)
    assert res_valid.passed is True
    assert res_valid.score == 1.0

    # Missing fields
    traj_missing = Trajectory(final_answer='{"name": "Alice"}')
    res_missing = scorer.measure(tc, traj_missing)
    assert res_missing.passed is False
    assert res_missing.score == 0.5

    # Malformed JSON
    traj_malformed = Trajectory(final_answer='```json {"name": "Alice"}')
    res_malformed = scorer.measure(tc, traj_malformed)
    assert res_malformed.passed is False
    assert res_malformed.score == 0.0


def test_rag_scorer_faithfulness():
    scorer = RAGFaithfulnessScorer(threshold=0.8)
    tc = TestCase(
        task_id="T4",
        layer="L1",
        instruction="What is the refund policy?",
        ground_truth=GroundTruth(golden_keywords=["7 days", "original packaging"]),
        context_chunks=["Returns are accepted within 7 days in original packaging."],
    )
    traj = Trajectory(final_answer="You can return the product within 7 days in original packaging.")
    res = scorer.measure(tc, traj)
    assert res.passed is True
    assert res.score == 1.0


def test_trajectory_scorer_infinite_loop_detection():
    scorer = TrajectoryMatchingScorer()
    tc = TestCase(
        task_id="T5",
        layer="L2",
        instruction="Query database",
        ground_truth=GroundTruth(expected_tools=[ToolCall(name="query_db", arguments={})]),
    )
    # Infinite loop: repeated 3 times sequentially
    traj_loop = Trajectory(
        steps=[
            Step(step_index=1, action=ToolCall(name="query_db", arguments={})),
            Step(step_index=2, action=ToolCall(name="query_db", arguments={})),
            Step(step_index=3, action=ToolCall(name="query_db", arguments={})),
        ]
    )
    res = scorer.measure(tc, traj_loop)
    assert res.passed is False
    assert res.score == 0.0
    assert "Infinite action loop" in res.reason


def test_position_swap_judge_consistency():
    scorer = PositionSwapJudgeScorer()
    res = scorer.measure_pair(
        instruction="Summarize AI",
        output_1="Artificial intelligence represents computer systems simulating human intelligence.",
        output_2="Short definition.",
    )
    assert res["consistent"] is True
    assert res["winner"] in ["MODEL_1", "MODEL_2", "TIE_OR_INCONSISTENT"]
