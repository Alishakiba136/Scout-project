#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.expression.text_to_speech import TermuxTextToSpeech


def main() -> int:
    if not os.path.exists("/data/data/com.termux"):
        print("NOT TESTED — requires POCO X3 / Android Termux")
        return 0

    speaker = TermuxTextToSpeech()
    message = "Hello. I am SCOUT."
    try:
        result = speaker.speak(message)
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1

    print(f"SCOUT says: {result}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
