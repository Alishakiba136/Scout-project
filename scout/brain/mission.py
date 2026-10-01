from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from scout.body import SafetyController

from .task_planner import TaskPlan


@dataclass
class MissionResult:
    """A single mission-run outcome produced by the execution loop."""

    goal: str
    steps: list[str]
    status: str
    reason: str = ""
    blocked: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class MissionLoop:
    """Deterministic execution loop that validates plans against the safety gate before acting."""

    def __init__(self, safety_controller: SafetyController | None = None) -> None:
        self.safety_controller = safety_controller or SafetyController()

    def run(self, plan: TaskPlan) -> MissionResult:
        if plan.requires_safety_check and not self.safety_controller.allow_action("mission"):
            return MissionResult(
                goal=plan.goal,
                steps=list(plan.steps),
                status="blocked",
                reason="emergency stop",
                blocked=True,
                metadata={"requires_safety_check": True},
            )

        return MissionResult(
            goal=plan.goal,
            steps=list(plan.steps),
            status="completed",
            reason="execution approved",
            blocked=False,
            metadata={"requires_safety_check": plan.requires_safety_check},
        )
