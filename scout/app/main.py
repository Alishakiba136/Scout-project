from __future__ import annotations

from .lifecycle import initialize_runtime
from .ui_server import build_robot_ui_state, start_robot_ui


def main() -> int:
    state = initialize_runtime(mode="development")
    print(f"SCOUT runtime ready: mode={state.mode}, ready={state.ready}")
    ui_state = build_robot_ui_state(mode=state.mode, ready=state.ready)
    ui_server = start_robot_ui(host="0.0.0.0", port=8000, state=ui_state)
    print(f"Robot UI ready at http://localhost:{ui_server.server_address[1]}")
    try:
        ui_server.serve_forever()
    except KeyboardInterrupt:
        pass
    ui_server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
