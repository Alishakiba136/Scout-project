from __future__ import annotations

import pytest

from scout.body.interface import SafetyController
from scout.tools.registry import ToolRegistry, ToolSpec


def test_tool_registry_executes_registered_safe_tool() -> None:
    registry = ToolRegistry()

    def say_hello(name: str) -> str:
        return f"hello {name}"

    registry.register(
        ToolSpec(
            name="say_hello",
            description="Greet a user.",
            input_schema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
            executor=say_hello,
            safety_classification="safe",
        )
    )

    assert registry.list_names() == ["say_hello"]
    assert registry.execute("say_hello", name="world") == "hello world"


def test_tool_registry_blocks_unsafe_tools() -> None:
    registry = ToolRegistry()

    def move_motor(direction: str) -> str:
        return f"moving {direction}"

    registry.register(
        ToolSpec(
            name="move_motor",
            description="Move hardware.",
            input_schema={"type": "object", "properties": {"direction": {"type": "string"}}, "required": ["direction"]},
            executor=move_motor,
            safety_classification="unsafe",
        )
    )

    with pytest.raises(ValueError, match="unsafe"):
        registry.execute("move_motor", direction="forward")


def test_safety_controller_blocks_hardware_when_emergency_stop_is_engaged() -> None:
    controller = SafetyController()

    assert controller.allow_action("move_arm") is True

    controller.emergency_stop()
    assert controller.allow_action("move_arm") is False

    controller.clear_emergency_stop()
    assert controller.allow_action("move_arm") is True
