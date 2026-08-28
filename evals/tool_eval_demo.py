"""
Tool Calling Evaluation Demo using Pytest & Evaluation Metrics.
Demonstrating exact matching, schema checking, and negative hallucination defense.
"""

import pytest
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class ToolCall:
    name: str
    input_parameters: Dict[str, Any]


@dataclass
class LLMTestCase:
    input: str
    actual_output: str
    tools_called: Optional[List[ToolCall]] = None
    expected_tools: Optional[List[ToolCall]] = None


class ToolCallPrecisionMetric:
    """
    Evaluates whether the Agent selected the correct tool and provided accurate arguments.
    Also handles negative samples (preventing tool hallucination on pure conversation).
    """

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.score = 0.0
        self.reason = ""

    def measure(self, test_case: LLMTestCase) -> float:
        expected_tools = test_case.expected_tools or []
        actual_tools = test_case.tools_called or []

        # 1. Negative Case: Expecting no tool calls
        if not expected_tools:
            if not actual_tools:
                self.score = 1.0
                self.reason = "Correctly refrained from invoking tools on non-tool query."
            else:
                self.score = 0.0
                self.reason = f"Tool Hallucination detected! Unexpectedly called: {[t.name for t in actual_tools]}"
            return self.score

        # 2. Positive Case: Compare tool names and arguments
        if not actual_tools:
            self.score = 0.0
            self.reason = "Agent failed to call any tool when tool execution was required."
            return self.score

        expected = expected_tools[0]
        actual = actual_tools[0]

        if expected.name != actual.name:
            self.score = 0.0
            self.reason = f"Wrong tool selected. Expected '{expected.name}', got '{actual.name}'."
            return self.score

        # Check required arguments
        if expected.input_parameters != actual.input_parameters:
            self.score = 0.5
            self.reason = f"Tool name matches, but arguments mismatch. Expected: {expected.input_parameters}, Actual: {actual.input_parameters}"
            return self.score

        self.score = 1.0
        self.reason = "Tool name and arguments match ground truth perfectly."
        return self.score

    def is_successful(self) -> bool:
        return self.score >= self.threshold


@pytest.mark.parametrize(
    "query, actual_tool_name, actual_params, expected_tool_name, expected_params",
    [
        (
            "帮我查一下明天北京的天气",
            "get_weather",
            {"city": "北京", "date": "2026-08-29"},
            "get_weather",
            {"city": "北京", "date": "2026-08-29"},
        ),
        (
            "你们公司几点下班？",
            None,
            None,
            None,
            None,
        ),
    ],
)
def test_agent_tool_calling(
    query, actual_tool_name, actual_params, expected_tool_name, expected_params
):
    actual_tools = (
        [ToolCall(name=actual_tool_name, input_parameters=actual_params)]
        if actual_tool_name
        else []
    )
    expected_tools = (
        [ToolCall(name=expected_tool_name, input_parameters=expected_params)]
        if expected_tool_name
        else []
    )

    test_case = LLMTestCase(
        input=query,
        actual_output="Simulated agent reply",
        tools_called=actual_tools,
        expected_tools=expected_tools,
    )

    metric = ToolCallPrecisionMetric(threshold=1.0)
    metric.measure(test_case)
    assert metric.is_successful(), f"Tool evaluation failed: {metric.reason}"


if __name__ == "__main__":
    test_agent_tool_calling(
        "帮我查一下明天北京的天气",
        "get_weather",
        {"city": "北京", "date": "2026-08-29"},
        "get_weather",
        {"city": "北京", "date": "2026-08-29"},
    )
    test_agent_tool_calling("你们公司几点下班？", None, None, None, None)
    print("All tool calling precision tests passed successfully!")
