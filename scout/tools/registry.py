from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    executor: Callable[..., Any]
    safety_classification: str = "safe"


class ToolRegistry:
    """Simple registry for safe, explicit tool registration."""

    def __init__(self) -> None:
        self.tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self.tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self.tools.get(name)

    def list_names(self) -> list[str]:
        return sorted(self.tools)
