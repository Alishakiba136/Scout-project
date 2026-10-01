from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .planner import plan_next_action


@dataclass
class CognitiveDecision:
    """A deterministic local-cognition decision record."""

    goal: str
    plan: list[str]
    reasoning: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


class ActiveCognition:
    """A simple local reasoning loop used before advanced ML or planning stacks."""

    def __init__(self, goal: str, context: dict[str, Any] | None = None) -> None:
        self.goal = goal
        self.context = context or {}

    def decide(self) -> CognitiveDecision:
        if not self.goal:
            plan = ["observe", "assess", "respond"]
            reasoning = (
                "No explicit objective was supplied, so the agent should first observe the environment "
                "and clarify before acting."
            )
            confidence = 0.45
        else:
            plan = plan_next_action(self.goal)
            reasoning = (
                f"Given the current objective '{self.goal}', the agent should observe the state, reason "
                "about the safest next step, and proceed with a bounded action plan."
            )
            confidence = 0.82 if self.context.get("mode") == "development" else 0.74

        return CognitiveDecision(
            goal=self.goal,
            plan=plan,
            reasoning=reasoning,
            confidence=confidence,
            metadata={"context": self.context},
        )
