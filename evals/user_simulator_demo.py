"""
Dynamic Multi-Turn User Simulator with Hidden Goal Card Demo.
Demonstrates simulating goal-shifts, ambiguity, and evaluating final task state.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UserGoalCard:
    goal: str
    budget: float
    taste_initial: str
    taste_shift: str
    shift_at_turn: int


class MockUserSimulator:
    """
    Simulates a demanding user with dynamic intent shifts.
    """

    def __init__(self, goal_card: UserGoalCard):
        self.card = goal_card
        self.turn = 0

    def respond(self, agent_message: str) -> str:
        self.turn += 1
        if self.turn == 1:
            return f"我想点一份{self.card.goal}，要{self.card.taste_initial}的。"
        elif self.turn == self.card.shift_at_turn:
            return f"等等，我嗓子不舒服，请帮我改成{self.card.taste_shift}！"
        elif "确认" in agent_message or "订单" in agent_message:
            return "没问题，请帮我提交下单吧！"
        return "好的。"


class MockAgent:
    """
    Simulates an Agent maintaining conversation state and slots.
    """

    def __init__(self):
        self.slots = {"dish": None, "taste": None, "price": 0.0}

    def chat(self, user_msg: str) -> str:
        if "麻婆豆腐" in user_msg:
            self.slots["dish"] = "麻婆豆腐"
            self.slots["price"] = 38.0

        if "微辣" in user_msg:
            self.slots["taste"] = "微辣"
        if "完全不辣" in user_msg or "不辣" in user_msg:
            self.slots["taste"] = "不辣"

        if self.slots["dish"] and self.slots["taste"]:
            return f"已为您记录：{self.slots['dish']}（{self.slots['taste']}），金额 {self.slots['price']} 元。请确认是否下单？"
        return "请问您需要什么口味？"


def test_multi_turn_user_simulation():
    goal_card = UserGoalCard(
        goal="麻婆豆腐",
        budget=50.0,
        taste_initial="微辣",
        taste_shift="不辣",
        shift_at_turn=2,
    )

    simulator = MockUserSimulator(goal_card)
    agent = MockAgent()

    # Turn 1
    user_msg1 = simulator.respond("")
    agent_reply1 = agent.chat(user_msg1)

    # Turn 2: User shifts taste from "微辣" to "不辣"
    user_msg2 = simulator.respond(agent_reply1)
    agent_reply2 = agent.chat(user_msg2)

    # Turn 3: User confirms
    user_msg3 = simulator.respond(agent_reply2)
    final_reply = agent.chat(user_msg3)

    # Assertions (Code Evaluation on Terminal State)
    assert agent.slots["dish"] == "麻婆豆腐", "Dish slot mismatch"
    assert agent.slots["taste"] == "不辣", "Agent failed to handle dynamic taste shift!"
    assert agent.slots["price"] <= goal_card.budget, "Budget exceeded"
    assert "确认" in agent_reply2, "Agent failed to confirm before ordering"


if __name__ == "__main__":
    test_multi_turn_user_simulation()
    print("Multi-turn User Simulator test passed successfully!")
