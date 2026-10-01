from __future__ import annotations

from pathlib import Path

from scout.perception.vision import SceneObservation, VisionPipeline


def test_scene_observation_tracks_core_image_metadata(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.jpg"
    image_path.write_bytes(
        b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x02\x00\x02\x03\x01\x22\x00\x02\x00\x00\x00"
    )

    observation = VisionPipeline().analyze_image(image_path)

    assert isinstance(observation, SceneObservation)
    assert observation.path == str(image_path)
    assert observation.width == 2
    assert observation.height == 2
    assert observation.format == "jpeg"
    assert observation.size_bytes > 0
    assert "sample" in observation.summary.lower()


def test_vision_pipeline_summarizes_unknown_images_without_crashing(tmp_path: Path) -> None:
    image_path = tmp_path / "unknown.bin"
    image_path.write_bytes(b"not-a-real-image")

    observation = VisionPipeline().analyze_image(image_path)

    assert observation.width is None
    assert observation.height is None
    assert observation.format == "unknown"
    assert "unknown" in observation.summary.lower()
