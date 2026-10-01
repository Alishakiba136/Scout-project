from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .goal_scheduler import GoalScheduler
from .task_planner import TaskPlan


@dataclass
class BehaviorResult:
    """A single scheduled behavior cycle produced by the agent loop."""

    goal: str
    plan: TaskPlan


class BehaviorLoop:
    """Deterministic orchestration layer that selects the next queued goal and plans it."""

    def __init__(self, scheduler: GoalScheduler | None = None) -> None:
        self.scheduler = scheduler or GoalScheduler()

    def enqueue(self, goal: str, priority: int = 0) -> str:
        self.scheduler.add_goal(goal, priority=priority)
        return goal

    def pending(self) -> list[str]:
        return self.scheduler.pending()

    def run_once(self, context: dict[str, Any] | None = None) -> BehaviorResult | None:
        plan = self.scheduler.next_task(context=context)
        if plan is None:
            return None
        return BehaviorResult(goal=plan.goal, plan=plan)

    def clear(self) -> None:
        self.scheduler.clear()
