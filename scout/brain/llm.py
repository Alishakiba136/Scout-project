from __future__ import annotations

import json
from typing import Any, Sequence
from urllib.request import Request, urlopen


class LLMClient:
    """Base interface for local LLM providers."""

    def generate(self, messages: Sequence[dict[str, str]], tools: Sequence[dict[str, Any]] | None = None) -> str:
        raise NotImplementedError("The local LLM provider is not implemented for this runtime.")


class LlamaCppClient(LLMClient):
    """HTTP client for a local llama.cpp server."""

    def __init__(self, server_url: str = "http://127.0.0.1:8080") -> None:
        self.server_url = server_url.rstrip("/")

    def generate(self, messages: Sequence[dict[str, str]], tools: Sequence[dict[str, Any]] | None = None) -> str:
        payload: dict[str, Any] = {"messages": list(messages), "stream": False}
        if tools:
            payload["tools"] = list(tools)

        req = Request(
            f"{self.server_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - surfaced to CLI/test scripts as runtime failure
            raise RuntimeError(f"Failed to contact local llama.cpp server at {self.server_url}: {exc}") from exc

        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError("Local llama.cpp server returned no choices.")

        message = choices[0].get("message", {})
        content = message.get("content")
        if content is None:
            return ""
        if isinstance(content, list):
            return "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return str(content)
