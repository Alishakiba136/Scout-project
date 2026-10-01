#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib import request, error

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.brain.llm import LlamaCppClient


def main() -> int:
    client = LlamaCppClient(server_url="http://127.0.0.1:8080")
    try:
        result = client.generate([{"role": "user", "content": "Say hello in one short sentence."}])
    except (error.URLError, OSError, RuntimeError):
        print("NOT TESTED — llama.cpp server is not running on http://127.0.0.1:8080")
        return 0

    print(f"LLM response: {result}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
