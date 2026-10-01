from __future__ import annotations

from scout.brain.session_memory import SessionMemory, SessionPlanner
from scout.memory.memory import MemoryStore


def test_session_memory_tracks_recent_goals() -> None:
    store = MemoryStore(database_path=":memory:")
    session = SessionMemory(store)

    session.record_goal("inspect the room")
    session.record_goal("close the window")

    recent = session.recent_goals(2)
    assert recent[0]["goal"] == "close the window"
    assert recent[1]["goal"] == "inspect the room"


def test_session_planner_adds_recent_goals_to_context() -> None:
    store = MemoryStore(database_path=":memory:")
    session = SessionMemory(store)
    session.record_goal("inspect the room")

    planner = SessionPlanner(session)
    plan = planner.plan("close the window")

    assert plan.goal == "close the window"
    assert plan.context["recent_goals"]
    assert "inspect the room" in plan.context["recent_goals"]


def test_session_planner_handles_empty_session() -> None:
    planner = SessionPlanner(SessionMemory(MemoryStore(database_path=":memory:")))

    plan = planner.plan("check the door")

    assert plan.context["recent_goals"] == []
    assert plan.steps[0] == "observe"
