from __future__ import annotations


class SafetyController:
    """Deterministic safety layer between cognitive intent and hardware execution."""

    def __init__(self) -> None:
        self.emergency_stop_engaged = False

    def emergency_stop(self) -> None:
        self.emergency_stop_engaged = True

    def clear_emergency_stop(self) -> None:
        self.emergency_stop_engaged = False

    def allow_action(self, action_name: str) -> bool:
        return action_name and not self.emergency_stop_engaged
