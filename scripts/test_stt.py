#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.perception.speech_to_text import LocalSpeechToText


def main() -> int:
    if not os.path.exists("/data/data/com.termux"):
        print("NOT TESTED — requires POCO X3 / Android Termux")
        return 0

    sample_path = Path("tmp/sample.wav")
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    sample_path.write_bytes(b"placeholder-audio")

    engine = LocalSpeechToText()
    result = engine.transcribe(sample_path)
    print(f"Transcribed text: {result}")
    print("PASS" if result else "FAIL")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
