from __future__ import annotations

import logging
from dataclasses import dataclass

from .config import load_config


@dataclass(slots=True)
class AppState:
    """Minimal application state used by the bootstrap layer."""

    mode: str = "development"
    ready: bool = False


def initialize_runtime(mode: str = "development") -> AppState:
    """Initialize logging and baseline configuration for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config = load_config()
    logger = logging.getLogger("scout.app")
    logger.info("SCOUT runtime initialize: mode=%s config=%s", mode, config.get("project", {}).get("name", "scout"))
    return AppState(mode=mode, ready=True)
