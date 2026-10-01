from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from scout.memory.memory import MemoryStore

from .task_planner import TaskPlan, TaskPlanner


@dataclass
class SessionMemory:
    """A lightweight session store that preserves recent goals in the local memory database."""

    store: MemoryStore
    session_subject: str = "session"

    def record_goal(self, goal: str) -> dict[str, Any]:
        if not goal:
            return {"goal": "", "subject": self.session_subject, "fact": "goal:", "source": "session"}
        return self.store.remember(subject=self.session_subject, fact=f"goal:{goal}", source="session")

    def recent_goals(self, limit: int = 5) -> list[dict[str, Any]]:
        if limit <= 0:
            return []

        rows = self.store.connection.execute(
            "SELECT fact, created_at FROM facts WHERE subject = ? AND fact LIKE 'goal:%' ORDER BY created_at DESC LIMIT ?",
            (self.session_subject, limit),
        ).fetchall()

        recent: list[dict[str, Any]] = []
        for row in rows:
            fact = row["fact"]
            goal = fact[len("goal:") :] if fact.startswith("goal:") else fact
            recent.append({"goal": goal, "created_at": row["created_at"]})
        return recent

    def clear(self) -> None:
        self.store.connection.execute("DELETE FROM facts WHERE subject = ? AND fact LIKE 'goal:%'", (self.session_subject,))
        self.store.connection.commit()


class SessionPlanner:
    """A planner that carries recent session goals alongside a normal plan context."""

    def __init__(self, session: SessionMemory | None = None, planner: TaskPlanner | None = None) -> None:
        self.session = session or SessionMemory(MemoryStore())
        self.planner = planner or TaskPlanner()

    def plan(self, goal: str, context: dict[str, Any] | None = None) -> TaskPlan:
        base_context = dict(context or {})
        recent_goals = [entry["goal"] for entry in self.session.recent_goals()]
        base_context["recent_goals"] = recent_goals
        return self.planner.plan(goal, context=base_context)
