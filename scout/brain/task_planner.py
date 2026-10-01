from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskPlan:
    """A minimal execution plan produced by the local task-planning layer."""

    goal: str
    steps: list[str]
    requires_safety_check: bool = False
    context: dict[str, Any] = field(default_factory=dict)


class TaskPlanner:
    """A deterministic planner that converts a high-level objective into a safe local plan."""

    def plan(self, goal: str, context: dict[str, Any] | None = None) -> TaskPlan:
        context = context or {}

        if not goal:
            return TaskPlan(
                goal="",
                steps=["observe", "assess", "respond"],
                requires_safety_check=False,
                context=context,
            )

        lowered = goal.lower()
        movement_keywords = {"move", "walk", "turn", "drive", "go", "approach", "reach"}
        requires_safety_check = any(keyword in lowered for keyword in movement_keywords)

        if requires_safety_check:
            steps = ["observe", "check_safety", "move", "verify"]
        else:
            steps = ["observe", "reason", "act", "report"]

        return TaskPlan(
            goal=goal,
            steps=steps,
            requires_safety_check=requires_safety_check,
            context=context,
        )
