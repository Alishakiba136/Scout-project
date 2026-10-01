from __future__ import annotations

from scout.body import SafetyController
from scout.brain.mission import MissionLoop, MissionResult
from scout.brain.task_planner import TaskPlan


def test_mission_loop_executes_safe_plan() -> None:
    loop = MissionLoop(safety_controller=SafetyController())
    plan = TaskPlan(
        goal="inspect the room",
        steps=["observe", "reason", "act", "report"],
        requires_safety_check=False,
    )

    result = loop.run(plan)

    assert isinstance(result, MissionResult)
    assert result.goal == "inspect the room"
    assert result.status == "completed"
    assert result.steps == ["observe", "reason", "act", "report"]
    assert result.blocked is False


def test_mission_loop_blocks_movement_plan_when_emergency_stop_is_engaged() -> None:
    safety = SafetyController()
    safety.emergency_stop()
    loop = MissionLoop(safety_controller=safety)
    plan = TaskPlan(
        goal="move to the door",
        steps=["observe", "check_safety", "move", "verify"],
        requires_safety_check=True,
    )

    result = loop.run(plan)

    assert result.status == "blocked"
    assert result.blocked is True
    assert result.reason == "emergency stop"


def test_mission_loop_handles_empty_plan() -> None:
    loop = MissionLoop()
    result = loop.run(TaskPlan(goal="", steps=["observe", "assess", "respond"]))

    assert result.status == "completed"
    assert result.steps == ["observe", "assess", "respond"]
    assert result.blocked is False
