from __future__ import annotations

from typing import Any

from .goal_queue import GoalQueue
from .task_planner import TaskPlan, TaskPlanner


class GoalScheduler:
    """Deterministic scheduler that selects the highest-priority goal and turns it into a plan."""

    def __init__(self, queue: GoalQueue | None = None, planner: TaskPlanner | None = None) -> None:
        self.queue = queue or GoalQueue()
        self.planner = planner or TaskPlanner()

    def add_goal(self, goal: str, priority: int = 0) -> str:
        self.queue.add(goal, priority=priority)
        return goal

    def pending(self) -> list[str]:
        return self.queue.pending()

    def next_task(self, context: dict[str, Any] | None = None) -> TaskPlan | None:
        if not self.queue.pending():
            return None
        goal = self.queue.next_goal()
        if goal is None:
            return None
        return self.planner.plan(goal, context={**(context or {}), "queued_goal": goal})

    def clear(self) -> None:
        self.queue.clear()
