from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True)
class GoalItem:
    """A queued goal with a priority and insertion order."""

    priority: int
    sequence: int = field(compare=False)
    goal: str = field(compare=False)


class GoalQueue:
    """Simple deterministic goal queue for local task prioritization."""

    def __init__(self) -> None:
        self._items: list[GoalItem] = []
        self._sequence = 0

    def add(self, goal: str, priority: int = 0) -> GoalItem:
        if not goal:
            raise ValueError("Goal cannot be empty")

        item = GoalItem(priority=priority, sequence=self._sequence, goal=goal)
        self._sequence += 1
        self._items.append(item)
        self._items.sort(key=lambda entry: (-entry.priority, entry.sequence))
        return item

    def next_goal(self) -> str | None:
        if not self._items:
            return None
        item = self._items.pop(0)
        return item.goal

    def pending(self) -> list[str]:
        return [item.goal for item in self._items]

    def clear(self) -> None:
        self._items.clear()
        self._sequence = 0
