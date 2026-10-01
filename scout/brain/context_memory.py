from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from scout.memory.memory import MemoryStore

from .task_planner import TaskPlan, TaskPlanner


@dataclass
class MemoryContext:
    """Flexible access layer around the local SQLite memory store."""

    store: MemoryStore

    def remember(self, subject: str, fact: str, source: str = "system") -> dict[str, Any]:
        return self.store.remember(subject=subject, fact=fact, source=source)

    def retrieve(self, subject: str | None = None, fact: str | None = None) -> list[dict[str, Any]]:
        return self.store.recall(subject=subject, fact=fact)


class MemoryAwarePlanner:
    """Task planner variant that folds relevant memory facts into the local plan context."""

    def __init__(self, memory: MemoryContext | None = None, planner: TaskPlanner | None = None) -> None:
        self.memory = memory or MemoryContext(MemoryStore())
        self.planner = planner or TaskPlanner()

    def _candidate_subjects(self, goal: str) -> list[str]:
        if not goal:
            return []

        tokens = [token.strip(".,!?;:\"'()[]{}") for token in goal.lower().split()]
        stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "in",
            "into",
            "is",
            "it",
            "of",
            "on",
            "or",
            "that",
            "the",
            "this",
            "to",
            "with",
        }
        subjects = [token for token in tokens if token and token not in stopwords]
        return list(dict.fromkeys(subjects))

    def plan(self, goal: str, context: dict[str, Any] | None = None) -> TaskPlan:
        base_context = dict(context or {})

        if not goal:
            base_context.setdefault("memory_facts", [])
            return self.planner.plan(goal, context=base_context)

        memory_facts: list[str] = []
        seen: set[str] = set()
        for subject in self._candidate_subjects(goal):
            for item in self.memory.retrieve(subject=subject):
                fact = item.get("fact")
                if fact and fact not in seen:
                    memory_facts.append(fact)
                    seen.add(fact)

        base_context["memory_facts"] = memory_facts
        return self.planner.plan(goal, context=base_context)
