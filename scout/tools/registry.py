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

    def invoke(self, **kwargs: Any) -> Any:
        return self.executor(**kwargs)


class ToolRegistry:
    """Simple registry for safe, explicit tool registration."""

    def __init__(self) -> None:
        self.tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self.tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self.tools.get(name)

    def is_safe(self, name: str) -> bool:
        spec = self.get(name)
        return spec is not None and spec.safety_classification != "unsafe"

    def execute(self, tool_name: str, **kwargs: Any) -> Any:
        spec = self.get(tool_name)
        if spec is None:
            raise KeyError(f"Unknown tool: {tool_name}")
        if not self.is_safe(tool_name):
            raise ValueError(f"Tool '{tool_name}' is marked unsafe and cannot be executed.")
        return spec.invoke(**kwargs)

    def list_names(self) -> list[str]:
        return sorted(self.tools)
