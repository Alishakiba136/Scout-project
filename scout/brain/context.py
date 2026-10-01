from __future__ import annotations


def build_context() -> dict[str, list[str] | str]:
    """Return the default context for the cognition loop."""
    return {
        "mode": "development",
        "cognitive_loop": [
            "observe",
            "perceive",
            "understand",
            "remember",
            "reason",
            "decide",
            "act",
            "observe",
        ],
    }
