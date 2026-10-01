from __future__ import annotations

from scout.brain.cognition import ActiveCognition, CognitiveDecision
from scout.brain.planner import plan_next_action


def test_plan_next_action_remains_goal_oriented() -> None:
    steps = plan_next_action("fetch a package")
    assert steps[0] == "observe"
    assert steps[-1] == "fetch a package"


def test_active_cognition_builds_explicit_decision() -> None:
    agent = ActiveCognition(goal="inspect the room", context={"mode": "development"})
    decision = agent.decide()

    assert isinstance(decision, CognitiveDecision)
    assert decision.goal == "inspect the room"
    assert decision.plan[0] == "observe"
    assert decision.reasoning
    assert 0.0 <= decision.confidence <= 1.0


def test_active_cognition_handles_empty_goal() -> None:
    agent = ActiveCognition(goal="")
    decision = agent.decide()

    assert decision.goal == ""
    assert decision.plan == ["observe", "assess", "respond"]
