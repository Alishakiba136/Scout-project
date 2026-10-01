from __future__ import annotations

import os
import shutil
import subprocess


class TextToSpeechInterface:
    """Abstract TTS interface intended to wrap Android Termux or local engines."""

    def __init__(self, voice: str | None = None) -> None:
        self.voice = voice

    def list_voices(self) -> list[str]:
        return [self.voice] if self.voice else []

    def speak(self, text: str) -> str:
        raise NotImplementedError("Speech synthesis is intentionally deferred until M1 hardware validation.")

    def stop(self) -> None:
        return None


class TermuxTextToSpeech(TextToSpeechInterface):
    """Android/Termux TTS wrapper for local speech output."""

    def __init__(self, voice: str | None = None) -> None:
        super().__init__(voice=voice or "default")

    def list_voices(self) -> list[str]:
        return ["default", "male", "female"]

    def speak(self, text: str) -> str:
        if not text:
            return ""

        if os.path.exists("/data/data/com.termux") and shutil.which("termux-tts-speak"):
            subprocess.run(["termux-tts-speak", text], check=True, capture_output=True, text=True)
            return text

        if shutil.which("espeak"):
            subprocess.run(["espeak", text], check=True, capture_output=True, text=True)
            return text

        if os.getenv("SCOUT_MODE") == "development":
            print(f"SCOUT says: {text}")
            return text

        raise RuntimeError("TTS unavailable in this environment; run on the POCO X3 or set development mode.")

    def stop(self) -> None:
        return None
