from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


class SpeechToTextEngine:
    """Interface for local/offline speech recognition providers."""

    def transcribe(self, audio_path: str | Path) -> str:
        raise NotImplementedError("Speech-to-text is intentionally deferred until the hardware target is available.")


class LocalSpeechToText(SpeechToTextEngine):
    """Local speech recognition wrapper with offline-first behavior."""

    def __init__(self, provider: str = "local") -> None:
        self.provider = provider

    def transcribe(self, audio_path: str | Path) -> str:
        audio_file = Path(audio_path)
        if not audio_file.exists():
            if os.getenv("SCOUT_MODE") == "development":
                return "hello scout"
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        if os.path.exists("/data/data/com.termux") and shutil.which("termux-speech-to-text"):
            result = subprocess.run(
                ["termux-speech-to-text", str(audio_file)],
                check=True,
                capture_output=True,
                text=True,
            )
            return (result.stdout or "").strip() or "transcription unavailable"

        if shutil.which("whisper"):
            result = subprocess.run(
                ["whisper", str(audio_file), "--output-dir", str(audio_file.parent)],
                check=True,
                capture_output=True,
                text=True,
            )
            return (result.stdout or "").strip() or "transcription unavailable"

        if os.getenv("SCOUT_MODE") == "development":
            return "hello scout"

        return "transcription unavailable"
