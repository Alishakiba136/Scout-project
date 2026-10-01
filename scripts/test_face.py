#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.expression.face import RobotFace


def main() -> int:
    face = RobotFace()
    states = face.cycle_demo()
    for state in states:
        face.set_expression(state)
        print(f"Expression: {state.value}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
