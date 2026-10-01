from scout.app.ui_server import RobotUIState, build_robot_ui_state, start_robot_ui


def test_robot_ui_state_contains_core_robot_features():
    state = build_robot_ui_state()

    assert isinstance(state, RobotUIState)
    assert state.name == "SCOUT"
    assert state.face_states
    assert "camera" in state.capabilities
    assert "microphone" in state.capabilities
    assert "speech" in state.capabilities
    assert "vision" in state.capabilities


def test_start_robot_ui_falls_back_to_next_free_port(monkeypatch):
    created = []

    class FakeServer:
        def __init__(self, address, handler):
            self.server_address = address
            self._handler = handler
            created.append(address)
            if len(created) == 1:
                raise OSError("Address already in use")

    monkeypatch.setattr("scout.app.ui_server.ThreadingHTTPServer", FakeServer)

    server = start_robot_ui(host="127.0.0.1", port=8000)

    assert server.server_address[1] == 8001
