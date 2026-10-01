#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.perception.microphone import TermuxMicrophone


def main() -> int:
    if not os.path.exists("/data/data/com.termux"):
        print("NOT TESTED — requires POCO X3 / Android Termux")
        return 0

    output_path = Path("tmp/microphone_record.wav")
    mic = TermuxMicrophone(device="default")
    try:
        result = mic.record_audio(str(output_path), duration_seconds=3)
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1

    mic.stop_recording()
    print(f"Microphone recording: {result}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
