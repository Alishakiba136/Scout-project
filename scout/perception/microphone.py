from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _is_termux_runtime() -> bool:
    return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ


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


class TermuxMicrophone(MicrophoneInterface):
    """Android/Termux microphone wrapper used for local recording."""

    def __init__(self, device: str | None = None) -> None:
        super().__init__(device=device)
        self.command = "termux-microphone-record"

    def get_microphone_status(self) -> dict[str, object]:
        return {
            "device": self.device,
            "recording": self.recording,
            "status": "ready" if _is_termux_runtime() else "development",
        }

    def record_audio(self, output_path: str, duration_seconds: int = 3) -> str:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        if _is_termux_runtime() and shutil.which(self.command):
            subprocess.run(
                [self.command, "-d", str(duration_seconds), str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.recording = True
            return str(output)

        if os.getenv("SCOUT_MODE") == "development":
            output.write_bytes(b"placeholder-audio")
            self.recording = True
            return str(output)

        raise RuntimeError("Microphone recording requires a POCO X3 / Android Termux runtime or development mode.")

    def stop_recording(self) -> None:
        if _is_termux_runtime() and shutil.which(self.command):
            subprocess.run([self.command, "-q"], check=False, capture_output=True, text=True)
        self.recording = False
