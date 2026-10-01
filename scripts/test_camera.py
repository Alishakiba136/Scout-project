#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.perception.camera import TermuxCamera


def main() -> int:
    if not os.path.exists("/data/data/com.termux"):
        print("NOT TESTED — requires POCO X3 / Android Termux")
        return 0

    output_path = Path("tmp/camera_capture.jpg")
    camera = TermuxCamera(camera_id=0)
    try:
        result = camera.capture_image(output_path)
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1

    print(f"Camera capture: {result}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
