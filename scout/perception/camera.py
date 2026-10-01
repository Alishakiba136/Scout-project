from __future__ import annotations

from pathlib import Path


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
