from __future__ import annotations


def plan_next_action(goal: str) -> list[str]:
    """Return a simple action plan for a given objective.

    This is intentionally lightweight and is only meant to establish the future
    cognitive decision layer before higher-level planning is implemented.
    """
    if not goal:
        return ["observe", "assess", "respond"]
    return ["observe", "reason", "decide", goal]
