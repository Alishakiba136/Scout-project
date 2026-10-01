from __future__ import annotations

from .lifecycle import initialize_runtime


def main() -> int:
    state = initialize_runtime(mode="development")
    print(f"SCOUT runtime ready: mode={state.mode}, ready={state.ready}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
