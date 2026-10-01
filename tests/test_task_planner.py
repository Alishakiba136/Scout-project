from __future__ import annotations

from scout.brain.task_planner import TaskPlan, TaskPlanner


def test_task_planner_creates_actionable_plan() -> None:
    planner = TaskPlanner()
    plan = planner.plan("inspect the room", context={"mode": "development"})

    assert isinstance(plan, TaskPlan)
    assert plan.goal == "inspect the room"
    assert plan.steps[0] == "observe"
    assert plan.steps[-1] in {"report", "respond"}
    assert plan.requires_safety_check is False


def test_task_planner_flags_movement_goals_for_safety_gate() -> None:
    planner = TaskPlanner()
    plan = planner.plan("move to the door", context={"mode": "development"})

    assert "move" in plan.steps
    assert plan.requires_safety_check is True


def test_task_planner_handles_empty_goal() -> None:
    planner = TaskPlanner()
    plan = planner.plan("", context={"mode": "development"})

    assert plan.goal == ""
    assert plan.steps == ["observe", "assess", "respond"]
    assert plan.requires_safety_check is False
