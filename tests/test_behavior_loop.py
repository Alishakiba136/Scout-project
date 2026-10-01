from __future__ import annotations

from scout.brain.behavior_loop import BehaviorLoop


def test_behavior_loop_runs_highest_priority_goal() -> None:
    loop = BehaviorLoop()
    loop.enqueue("inspect the room")
    loop.enqueue("close the window", priority=5)
    loop.enqueue("check battery", priority=2)

    result = loop.run_once()

    assert result is not None
    assert result.goal == "close the window"
    assert result.plan.goal == "close the window"
    assert result.plan.steps[0] == "observe"
    assert loop.pending() == ["check battery", "inspect the room"]


def test_behavior_loop_returns_none_when_empty() -> None:
    loop = BehaviorLoop()

    assert loop.run_once() is None
    assert loop.pending() == []
