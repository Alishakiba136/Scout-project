from __future__ import annotations

from scout.brain.goal_queue import GoalQueue


def test_goal_queue_prioritizes_higher_priority_goals() -> None:
    queue = GoalQueue()
    queue.add("inspect the room")
    queue.add("close the window", priority=5)
    queue.add("check battery", priority=2)

    assert queue.next_goal() == "close the window"
    assert queue.pending() == ["check battery", "inspect the room"]


def test_goal_queue_returns_none_when_empty() -> None:
    queue = GoalQueue()

    assert queue.next_goal() is None
    assert queue.pending() == []
