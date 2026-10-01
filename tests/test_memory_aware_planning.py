from __future__ import annotations

from scout.brain.context_memory import MemoryAwarePlanner, MemoryContext
from scout.memory.memory import MemoryStore


def test_memory_context_retrieves_subject_facts() -> None:
    store = MemoryStore(database_path=":memory:")
    memory = MemoryContext(store)
    memory.remember("robot", "battery is healthy")

    facts = memory.retrieve("robot")
    assert any("battery is healthy" in fact["fact"] for fact in facts)


def test_memory_aware_planner_injects_relevant_memory_into_context() -> None:
    store = MemoryStore(database_path=":memory:")
    store.remember("room", "window is open")
    planner = MemoryAwarePlanner(memory=MemoryContext(store))

    plan = planner.plan("inspect the room")

    assert plan.goal == "inspect the room"
    assert "window is open" in plan.context["memory_facts"]
    assert plan.steps[0] == "observe"


def test_memory_aware_planner_handles_missing_memory_gracefully() -> None:
    planner = MemoryAwarePlanner(memory=MemoryContext(MemoryStore(database_path=":memory:")))

    plan = planner.plan("check the hallway")

    assert plan.context["memory_facts"] == []
    assert plan.steps[0] == "observe"
