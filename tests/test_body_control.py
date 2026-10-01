from __future__ import annotations

import pytest

from scout.body import BodyController, ESP32Controller, SafetyController


def test_body_controller_approves_motor_move() -> None:
    controller = BodyController()
    payload = controller.move("forward", speed=42)

    assert payload["action"] == "move"
    assert payload["direction"] == "forward"
    assert payload["speed"] == 42
    assert payload["status"] == "approved"


def test_body_controller_rejects_when_emergency_stop_is_engaged() -> None:
    controller = BodyController(safety_controller=SafetyController())
    controller.safety_controller.emergency_stop()

    with pytest.raises(RuntimeError, match="emergency stop"):
        controller.move("left", speed=10)


def test_esp32_controller_serializes_safe_command() -> None:
    controller = ESP32Controller()
    payload = controller.command("stop")

    assert payload["device"] == "esp32"
    assert payload["action"] == "stop"
    assert payload["status"] == "queued"
