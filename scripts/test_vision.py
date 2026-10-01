#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.perception.vision import VisionPipeline


def main() -> int:
    sample = Path("tmp/vision_sample.jpg")
    sample.parent.mkdir(parents=True, exist_ok=True)
    sample.write_bytes(
        b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x02\x00\x02\x03\x01\x22\x00\x02\x00\x00\x00"
    )

    observation = VisionPipeline().analyze_image(sample)
    print(observation.summary)
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
