"""
Robustness, JSON Schema Integrity, and Exception Fallback Evaluation Demo.
Demonstrates automated testing for prompt perturbation, schema compliance, and API 500 error fallback.
"""

import pytest
import json
from dataclasses import dataclass
from typing import Dict, Any, Optional


class MockAgentWithFallback:
    """
    Simulates a production Agent with error-handling guardrails and prompt perturbation tolerance.
    """

    def __init__(self, simulate_tool_failure: bool = False):
        self.simulate_tool_failure = simulate_tool_failure
        self.fallback_triggered = False

    def process_order(self, query: str) -> Dict[str, Any]:
        # Clean perturbation (trim spaces)
        clean_query = " ".join(query.strip().split())

        if "麻婆豆腐" not in clean_query:
            return {
                "status": "rejected",
                "error": "Out of domain request",
                "message": "抱歉，目前仅支持店内招牌菜品预订。",
            }

        # Simulate External Tool Call (e.g. Payment/Inventory API)
        if self.simulate_tool_failure:
            self.fallback_triggered = True
            # Graceful Fallback (Never throw 500 or raw exception trace to end user)
            return {
                "status": "fallback",
                "dish_name": "麻婆豆腐",
                "price": 38.0,
                "message": "系统网络繁忙，已为您暂存订单草稿，请稍后重试或联系人工客服。",
            }

        return {
            "status": "success",
            "dish_name": "麻婆豆腐",
            "price": 38.0,
            "message": "下单成功！",
        }


def test_prompt_perturbation_robustness():
    """
    Verifies that prompt perturbations (extra spaces, punctuation changes) do not break the Agent.
    """
    agent = MockAgentWithFallback(simulate_tool_failure=False)

    queries = [
        "我要一份麻婆豆腐",
        "  我要一份   麻婆豆腐   ",
        "我要一份麻婆豆腐！！！",
        "帮我点单：麻婆豆腐，谢谢。",
    ]

    for q in queries:
        res = agent.process_order(q)
        assert res["status"] == "success", f"Failed on perturbed query: '{q}'"
        assert res["dish_name"] == "麻婆豆腐"
        assert isinstance(res["price"], float)


def test_json_schema_structural_integrity():
    """
    Verifies that model output strictly adheres to the required JSON schema keys and types.
    """
    agent = MockAgentWithFallback(simulate_tool_failure=False)
    res = agent.process_order("我要一份麻婆豆腐")

    required_keys = {"status", "dish_name", "price", "message"}
    assert required_keys.issubset(
        res.keys()
    ), f"Missing required keys in schema: {required_keys - set(res.keys())}"
    assert isinstance(res["status"], str)
    assert isinstance(res["price"], (int, float))


def test_tool_failure_graceful_fallback():
    """
    Verifies that when external tools crash (500/timeout), the Agent triggers fallback and does NOT leak exceptions.
    """
    failing_agent = MockAgentWithFallback(simulate_tool_failure=True)
    res = failing_agent.process_order("我要一份麻婆豆腐")

    # 1. Fallback flag triggered
    assert failing_agent.fallback_triggered is True
    assert res["status"] == "fallback"

    # 2. No raw traceback leakage
    msg = res["message"]
    assert "Traceback" not in msg
    assert "Exception" not in msg
    assert "500" not in msg
    assert "人工客服" in msg or "稍后重试" in msg


if __name__ == "__main__":
    test_prompt_perturbation_robustness()
    test_json_schema_structural_integrity()
    test_tool_failure_graceful_fallback()
    print(
        "All Robustness, Schema Integrity & Fallback tests passed successfully!"
    )
