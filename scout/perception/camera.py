from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _is_termux_runtime() -> bool:
    return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ


class CameraInterface:
    """Abstract camera interface for future Android and desktop deployments."""

    def __init__(self, camera_id: int = 0, resolution: str = "1280x720") -> None:
        self.camera_id = camera_id
        self.resolution = resolution

    def list_cameras(self) -> list[int]:
        return [self.camera_id]

    def get_camera_info(self) -> dict[str, object]:
        return {"camera_id": self.camera_id, "resolution": self.resolution, "status": "not_implemented"}

    def capture_image(self, output_path: str | Path | None = None) -> str:
        if output_path is None:
            output_path = Path("tmp/capture.jpg")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        raise NotImplementedError("Camera capture is intentionally deferred until M1 hardware validation.")


class TermuxCamera(CameraInterface):
    """Android/Termux camera wrapper used by the phone runtime."""

    def __init__(self, camera_id: int = 0, resolution: str = "1280x720") -> None:
        super().__init__(camera_id=camera_id, resolution=resolution)
        self.command = "termux-camera-photo"

    def list_cameras(self) -> list[int]:
        if _is_termux_runtime():
            return [0, 1]
        return [self.camera_id]

    def get_camera_info(self) -> dict[str, object]:
        status = "ready" if _is_termux_runtime() else "development"
        return {"camera_id": self.camera_id, "resolution": self.resolution, "status": status}

    def capture_image(self, output_path: str | Path | None = None) -> str:
        if output_path is None:
            output_path = Path("tmp/capture.jpg")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if _is_termux_runtime() and shutil.which(self.command):
            subprocess.run(
                [self.command, "-c", str(self.camera_id), str(output_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            return str(output_path)

        if os.getenv("SCOUT_MODE") == "development":
            output_path.write_bytes(b"placeholder-jpeg")
            return str(output_path)

        raise RuntimeError("Camera capture requires a POCO X3 / Android Termux runtime or development mode.")
