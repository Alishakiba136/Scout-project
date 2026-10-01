from __future__ import annotations

from scout.brain.goal_scheduler import GoalScheduler


def test_goal_scheduler_selects_highest_priority_goal() -> None:
    scheduler = GoalScheduler()
    scheduler.add_goal("inspect the room")
    scheduler.add_goal("close the window", priority=5)
    scheduler.add_goal("check battery", priority=2)

    plan = scheduler.next_task()

    assert plan is not None
    assert plan.goal == "close the window"
    assert scheduler.pending() == ["check battery", "inspect the room"]


def test_goal_scheduler_returns_none_when_queue_is_empty() -> None:
    scheduler = GoalScheduler()

    assert scheduler.next_task() is None
    assert scheduler.pending() == []
