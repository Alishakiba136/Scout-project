from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SceneObservation:
    """A small, local-first image observation record used by the perception layer."""

    path: str
    format: str = "unknown"
    width: int | None = None
    height: int | None = None
    size_bytes: int = 0
    tags: list[str] = field(default_factory=list)
    summary: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "format": self.format,
            "width": self.width,
            "height": self.height,
            "size_bytes": self.size_bytes,
            "tags": list(self.tags),
            "summary": self.summary,
        }


class VisionPipeline:
    """Stage-1 perception layer for image metadata and basic scene summaries."""

    def analyze_image(self, image_path: str | Path) -> SceneObservation:
        path = Path(image_path)
        file_size = path.stat().st_size if path.exists() else 0
        image_format = self._detect_format(path)
        width, height = self._read_dimensions(path, image_format)
        tags = self._guess_tags(width, height, file_size, image_format)
        summary = self._build_summary(path, image_format, width, height, tags)

        return SceneObservation(
            path=str(path),
            format=image_format,
            width=width,
            height=height,
            size_bytes=file_size,
            tags=tags,
            summary=summary,
        )

    @staticmethod
    def _detect_format(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            return "jpeg"
        if suffix == ".png":
            return "png"
        if suffix == ".gif":
            return "gif"

        try:
            header = path.read_bytes()[:8]
        except OSError:
            return "unknown"

        if header.startswith(b"\xff\xd8"):
            return "jpeg"
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if header.startswith((b"GIF87a", b"GIF89a")):
            return "gif"
        return "unknown"

    @staticmethod
    def _read_dimensions(path: Path, image_format: str) -> tuple[int | None, int | None]:
        if image_format not in {"jpeg", "jpg"}:
            return None, None
        try:
            data = path.read_bytes()
        except OSError:
            return None, None

        if len(data) < 10 or not data.startswith(b"\xff\xd8"):
            return None, None

        idx = 2
        while idx < len(data) - 1:
            if data[idx] != 0xFF:
                idx += 1
                continue
            marker = data[idx : idx + 2]
            if marker == b"\xff\xc0":
                if idx + 9 > len(data):
                    return None, None
                height = int.from_bytes(data[idx + 5 : idx + 7], byteorder="big")
                width = int.from_bytes(data[idx + 7 : idx + 9], byteorder="big")
                return width, height
            if marker in {b"\xff\xd9", b"\xff\xda"}:
                break
            if idx + 4 > len(data):
                break
            section_length = int.from_bytes(data[idx + 2 : idx + 4], byteorder="big")
            idx += 2 + section_length

        return None, None

    @staticmethod
    def _guess_tags(width: int | None, height: int | None, file_size: int, image_format: str) -> list[str]:
        tags: list[str] = []
        if image_format != "unknown":
            tags.append(image_format)
        if width and height:
            tags.append(f"{width}x{height}")
        if file_size > 0:
            tags.append("nonempty")
        return tags

    @staticmethod
    def _build_summary(path: Path, image_format: str, width: int | None, height: int | None, tags: list[str]) -> str:
        name = path.name
        if image_format == "unknown":
            if width is None and height is None:
                return f"{name} is an unknown image type; no dimensions were detected."
            return f"{name} is an {image_format} image with a detected scene size of {width}x{height}."

        if width and height:
            return f"{name} is a {image_format} image at {width}x{height}; tags: {', '.join(tags)}."
        return f"{name} is a {image_format} image; tags: {', '.join(tags)}."
