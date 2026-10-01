from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.example.toml"


def resolve_config_path(path: str | Path | None = None) -> Path:
    """Return the active configuration path for the current environment."""
    if path is not None:
        return Path(path)

    project_root = Path(__file__).resolve().parents[2]
    for candidate in (
        project_root / "config" / "config.toml",
        project_root / "config" / "config.example.toml",
    ):
        if candidate.exists():
            return candidate
    return DEFAULT_CONFIG_PATH


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load a TOML configuration file.

    The project defaults to the example config when a local config is not present.
    """
    config_path = resolve_config_path(path)
    with config_path.open("rb") as handle:
        data = tomllib.load(handle)
    return dict(data)
