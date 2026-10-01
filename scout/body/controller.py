from __future__ import annotations

from typing import Any

from .interface import SafetyController


class BodyController:
    """Deterministic hardware controller for body-level movement commands."""

    def __init__(self, safety_controller: SafetyController | None = None) -> None:
        self.safety_controller = safety_controller or SafetyController()

    def _assert_safe(self, action_name: str) -> None:
        if not self.safety_controller.allow_action(action_name):
            raise RuntimeError(f"Action '{action_name}' blocked by emergency stop.")

    def move(self, direction: str, speed: int = 0, **kwargs: Any) -> dict[str, Any]:
        self._assert_safe("move")
        if not direction:
            raise ValueError("direction is required")
        payload = {
            "action": "move",
            "direction": direction,
            "speed": int(speed),
            "status": "approved",
        }
        payload.update(kwargs)
        return payload

    def stop(self) -> dict[str, Any]:
        self._assert_safe("stop")
        return {"action": "stop", "status": "approved"}

    def turn(self, direction: str, angle: int = 90) -> dict[str, Any]:
        self._assert_safe("turn")
        return {"action": "turn", "direction": direction, "angle": int(angle), "status": "approved"}


class ESP32Controller(BodyController):
    """Small serializable interface for a future ESP32 driver device."""

    def command(self, action: str, **kwargs: Any) -> dict[str, Any]:
        self._assert_safe(action)
        payload = {"device": "esp32", "action": action, "status": "queued"}
        payload.update(kwargs)
        return payload
