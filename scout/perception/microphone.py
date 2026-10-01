from __future__ import annotations


class MicrophoneInterface:
    """Abstract microphone interface for future Android and desktop testing."""

    def __init__(self, device: str | None = None) -> None:
        self.device = device
        self.recording = False

    def get_microphone_status(self) -> dict[str, object]:
        return {"device": self.device, "recording": self.recording, "status": "not_implemented"}

    def record_audio(self, output_path: str, duration_seconds: int = 3) -> str:
        self.recording = True
        raise NotImplementedError("Audio capture is intentionally deferred until M1 hardware validation.")

    def stop_recording(self) -> None:
        self.recording = False
