from __future__ import annotations

from enum import Enum


class FaceExpression(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    HAPPY = "happy"
    CONFUSED = "confused"
    SURPRISED = "surprised"
    SLEEPING = "sleeping"
    ERROR = "error"


class RobotFace:
    """Simple face controller interface for future UI updates."""

    def __init__(self) -> None:
        self.current = FaceExpression.IDLE

    def set_expression(self, expression: FaceExpression | str) -> FaceExpression:
        value = FaceExpression(expression) if isinstance(expression, str) else expression
        self.current = value
        return self.current

    def cycle_demo(self) -> list[FaceExpression]:
        return [
            FaceExpression.IDLE,
            FaceExpression.LISTENING,
            FaceExpression.THINKING,
            FaceExpression.SPEAKING,
            FaceExpression.HAPPY,
            FaceExpression.CONFUSED,
            FaceExpression.SURPRISED,
            FaceExpression.SLEEPING,
            FaceExpression.ERROR,
        ]
