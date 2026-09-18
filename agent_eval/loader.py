# -*- coding: utf-8 -*-
import json
from typing import List, Dict, Any
from agent_eval.schema import TestCase, GroundTruth, ToolCall


class DatasetLoader:
    """
    Standard dataset loader for Agent Eval JSON benchmarks.
    Parses unified AgentEvalCaseProtocol JSON documents into strongly-typed TestCase objects.
    """

    @staticmethod
    def load_from_file(file_path: str) -> List[TestCase]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON array of test cases, got {type(data).__name__}")

        cases = []
        for item in data:
            gt_data = item.get("ground_truth", {})
            expected_tools = []
            if "expected_tools" in gt_data and gt_data["expected_tools"] is not None:
                for t in gt_data["expected_tools"]:
                    expected_tools.append(ToolCall(name=t["name"], arguments=t.get("arguments", {})))
            else:
                expected_tools = None

            gt = GroundTruth(
                expected_tools=expected_tools,
                expected_state_diff=gt_data.get("expected_state_diff"),
                golden_keywords=gt_data.get("golden_keywords"),
                required_fields=gt_data.get("required_fields"),
                min_steps=gt_data.get("min_steps"),
                max_steps=gt_data.get("max_steps"),
            )

            tc = TestCase(
                task_id=item["task_id"],
                layer=item.get("layer", "L1"),
                instruction=item["instruction"],
                ground_truth=gt,
                context_chunks=item.get("context_chunks"),
                metadata=item.get("metadata", {}),
            )
            cases.append(tc)

        return cases
