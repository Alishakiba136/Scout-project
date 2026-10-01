#!/usr/bin/env python3
from __future__ import annotations

import os
import platform
import shutil
import socket
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.app.config import load_config



def _available(command: str) -> bool:
    return shutil.which(command) is not None


def _termux_check() -> bool:
    return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ


def _database_check(database_path: str) -> bool:
    try:
        connection = sqlite3.connect(database_path)
        connection.close()
        return True
    except sqlite3.Error:
        return False


def _network_check() -> bool:
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=2):
            return True
    except OSError:
        return False


def run_doctor() -> dict[str, object]:
    config = load_config()
    paths = config.get("paths", {})
    database_path = str(PROJECT_ROOT / paths.get("database_path", "./scout.db")).replace("./", "")
    termux_present = _termux_check()

    checks = {
        "python": sys.version_info >= (3, 10),
        "architecture": platform.machine().lower() in {"arm64", "aarch64", "amd64", "x86_64"},
        "operating_system": platform.system(),
        "termux": termux_present,
        "camera": termux_present and (_available("termux-camera-photo") or _available("ffmpeg")),
        "microphone": termux_present and (_available("termux-microphone-record") or _available("ffmpeg") or _available("arecord")),
        "tts": termux_present and (_available("termux-tts-speak") or _available("espeak") or _available("spd-say")),
        "stt": termux_present and (_available("ffmpeg") or _available("pocketsphinx_continuous") or _available("whisper")),
        "storage_permissions": os.access(PROJECT_ROOT, os.W_OK),
        "network": _network_check(),
        "local_model": Path(paths.get("model_dir", "models")).exists() or Path(PROJECT_ROOT / "models").exists(),
        "llama_cpp": _available("llama-server") or _available("llama-cli"),
        "database": _database_check(database_path),
    }

    core_ready = all(
        checks[key]
        for key in ["python", "architecture", "storage_permissions", "database"]
    )
    hardware_ready = termux_present and all(checks[key] for key in ["camera", "microphone", "tts", "stt"])
    checks["overall"] = "READY" if core_ready else "NOT READY"
    checks["hardware_status"] = "READY" if hardware_ready else "REQUIRES DEVICE"
    checks["recommended_fix"] = (
        "Run this script on the POCO X3 / Android Termux runtime to validate camera, microphone, STT, and TTS. "
        "The desktop workstation cannot confirm those hardware checks."
        if not hardware_ready
        else "No hardware fix required on this system."
    )
    return checks


def _format_status(label: str, value: bool, note: str = "") -> str:
    symbol = "✓" if value else "✗"
    return f"{label:<18} {symbol} {note}".rstrip()


def main() -> int:
    print("SCOUT SYSTEM CHECK")
    print("=" * 18)
    result = run_doctor()

    print(_format_status("Python", bool(result["python"]), f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"))
    print(_format_status("Architecture", bool(result["architecture"]), str(platform.machine())))
    print(_format_status("Termux", bool(result["termux"]), "Android runtime" if result["termux"] else "not detected"))
    print(_format_status("Camera", bool(result["camera"]), "available" if result["camera"] else "requires POCO X3"))
    print(_format_status("Microphone", bool(result["microphone"]), "available" if result["microphone"] else "requires POCO X3"))
    print(_format_status("Speech-to-text", bool(result["stt"]), "available" if result["stt"] else "requires device"))
    print(_format_status("Text-to-speech", bool(result["tts"]), "available" if result["tts"] else "requires device"))
    print(_format_status("Local LLM", bool(result["llama_cpp"] or result["local_model"]), "available" if result["llama_cpp"] or result["local_model"] else "model or server missing"))
    print(_format_status("SQLite", bool(result["database"]), "database ready" if result["database"] else "database unavailable"))
    print(_format_status("Storage", bool(result["storage_permissions"]), "writable" if result["storage_permissions"] else "read-only"))
    print(_format_status("Network", bool(result["network"]), "connected" if result["network"] else "offline"))

    print()
    print(f"Overall: {result['overall']}")
    print(f"Hardware: {result['hardware_status']}")
    print(f"Fix: {result['recommended_fix']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
